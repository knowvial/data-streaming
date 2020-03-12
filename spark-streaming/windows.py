import sys
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import window
from pyspark.sql.functions import udf
import time
import datetime

if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        print("Usage: spark-submit windows.py <hostname> <port> <option>", file=sys.stderr)
        exit(-1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    option = sys.argv[3]

    spark = SparkSession\
        .builder\
        .appName("NetcatWordCount")\
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Create DataFrame representing the stream of input lines from connection to host:port
    # We're reading from the socket on the port where netcat is listening
    lines = spark\
        .readStream\
        .format('socket')\
        .option('host', host)\
        .option('port', port)\
        .load()

    nums = lines.select(
        explode(
            split(lines.value, ' ')
        ).alias('num')
    )
    #nums = nums.selectExpr("cast(num as int) num")
    def add_timestamp():
         ts = time.time()
         timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
         return timestamp

    add_timestamp_udf = udf(add_timestamp, StringType())
    numsTs = nums.withColumn("timestamp", add_timestamp_udf())

    if option == 'stateless':
      query = nums.filter(nums.num > 65)\
                .writeStream\
                .outputMode('append')\
                .trigger(processingTime="10 seconds")\
                .format('console')\
                .start()
    elif option == 'rolling':
        windowedCounts = numsTs.agg({"num": "sum"})\
                        .withColumnRenamed("sum(num)", "TotalVehicles")

        query = windowedCounts.writeStream\
                              .outputMode("complete")\
                              .format("console")\
                              .option("truncate","false")\
                              .start()\
                              .awaitTermination()
    elif option == 'tumble':

        # window(timeColumn, windowDuration, slideDuration=None, startTime=None)
        # timeColumn gives the time field to use when creating a window
        # windowDuration gives the length of the window
        # slideDuration is the gap between each window (Windows can overlap)
        # slideDuration must be <= windowDuration
        # The #convictions for a particular window will likely increase with each batch of files processed - 
        # this is because more timestamps within that window will be encountered in the new batch
        windowedCounts = numsTs.groupBy(
                          window(numsTs.timestamp, "10 seconds"))\
                        .agg({"num": "sum"})\
                        .withColumnRenamed("sum(num)", "TotalVehicles")\
                        .orderBy('window', ascending=False)

        # Write output to the console
        query = windowedCounts.writeStream\
                              .outputMode("complete")\
                              .format("console")\
                              .option("truncate","false")\
                              .start()\
                              .awaitTermination()

    elif option == 'sliding':
      windowedCount = numsTs.groupBy(window(numsTs.timestamp, "10 seconds", "5 seconds"))\
        .agg({"num": "sum"})\
        .withColumnRenamed("sum(num)", "TotalVehicles")\
        .orderBy('window', ascending=False)

      query = windowedCount.writeStream\
                  .outputMode("complete")\
                  .format("console")\
                  .option("truncate", "false")\
                  .start()\
                  .awaitTermination()

    query.awaitTermination()