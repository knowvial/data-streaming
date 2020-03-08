from pyspark.sql.types import *
from pyspark.sql import SparkSession


if __name__ == "__main__":
    sparkSession = SparkSession.builder.master("local")\
        .appName("SparkStreamingAppendMode")\
        .getOrCreate()

    # ERROR log level will generate fewer lines of output compared to INFO and DEBUG
    sparkSession.sparkContext.setLogLevel("ERROR")

    # InferSchema not yet available in spark structured streaming
    # (it is available in static dataframes)
    # We explicity state the schema of the input data
    schema = StructType([StructField("product", StringType(), True),
                         StructField("city", StringType(), True),
                         StructField("state", StringType(), True),
                         StructField("country", StringType(), True),
                         StructField("sales", StringType(), True)
                         ])

    # Read stream into a dataframe
    # Since the csv data includes a header row, we specify that here
    # We state the schema to use and the location of the csv files
    fileStreamDF = sparkSession.readStream\
                               .option("header", "false")\
                               .schema(schema)\
                               .csv("./datasets/droplocation")

    # Check whether input data is streaming or not
    print(" ")
    print("Is the stream ready?")
    print(fileStreamDF.isStreaming)

    # Print Schema
    print(" ")
    print("Schema of the input stream: ")
    print(fileStreamDF.printSchema)

    # Create a trimmed version of the input dataframe with specific columns
    # We cannot sort a DataFrame unless aggregate is used, so no sorting here
    trimmedDF = fileStreamDF.select(
        fileStreamDF.product,
        fileStreamDF.city,
        fileStreamDF.state,
        fileStreamDF.country
    )

    # We run in append mode, so only new rows are processed,
    # and existing rows in Result Table are not affected
    # The output is written to the console
    # We set truncate to false. If true, the output is truncated to 20 chars
    # Explicity state number of rows to display. Default is 20
    query = fileStreamDF.writeStream\
        .outputMode("append")\
        .format("console")\
        .option("truncate", "false")\
        .option("numRows", 30)\
        .start()\
        .awaitTermination()

    # 3: Complete mode
    # query = fileStreamDF.writeStream\
    #     .outputMode("complete")\
    #     .format("console")\
    #     .option("truncate", "false")\
    #     .option("numRows", 30)\
    #     .start()\
    #     .awaitTermination()

    # 4: Aggregate mode

    # salesDf = fileStreamDF.groupBy("state")\
    #                                   .agg({"sales": "sum"})\
    #                                   .withColumnRenamed("sum(sales)", "tot_sales")\
    #                                   .orderBy("tot_sales", ascending=False)

    # # Write out our dataframe to the console
    # query = salesDf.writeStream\
    #                   .outputMode("complete")\
    #                   .format("console")\
    #                   .option("truncate", "false")\
    #                   .option("numRows", 30)\
    #                   .start()\
    #                   .awaitTermination()