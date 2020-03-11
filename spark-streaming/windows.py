import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

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
    nums = nums.selectExpr("cast(num as int) num")

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
        print('tumble')
    elif option == 'sliding':
        print('sliding')

    query.awaitTermination()