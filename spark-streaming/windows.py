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
      timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
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
      print('rolling')
    elif option == 'tumble':
      windowedCount = numsTs.groupBy(window(numsTs.timestamp, "60 seconds", "60 seconds"))\
                          .agg({"num": "sum"})\
                          .withColumnRenamed("sum(num)", "TotalVehicles")\
                          .orderBy('TotalVehicles', ascending=False)
      
      query = windowedCount.writeStream\
                  .outputMode("complete")\
                  .format("console")\
                  .option("truncate", "false")\
                  .start()\
                  .awaitTermination()

    elif option == 'sliding':
      numsTs.groupBy(window(numsTs.timestamp, "60 seconds", "30 seconds"))\
        .agg({"num": "sum"})\
        .withColumnRenamed("sum(num)", "TotalVehicles")\
        .orderBy('TotalVehicles', ascending=False)

      query = windowedCount.writeStream\
                  .outputMode("complete")\
                  .format("console")\
                  .option("truncate", "false")\
                  .start()\
                  .awaitTermination()

    query.awaitTermination()