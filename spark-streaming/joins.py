from pyspark.sql.types import *
from pyspark.sql import SparkSession


if __name__ == "__main__":

    sparkSession = SparkSession.builder.master("local")\
                              .appName("SparkStreamingSQLQuery")\
                              .getOrCreate()

    sparkSession.sparkContext.setLogLevel("ERROR")

    schema = StructType([StructField("product", StringType(), True),
                         StructField("city", StringType(), True),
                         StructField("state", StringType(), True),
                         StructField("country", StringType(), True),
                         StructField("sales", StringType(), True)
                         ])

    fileStreamDF = sparkSession.readStream\
                               .option("header", "false")\
                               .option("maxFilesPerTrigger", 2)\
                               .schema(schema)\
                               .csv("./datasets/droplocation")

    headsSchema = StructType([StructField("regional_head", StringType(), True),
                         StructField("city", StringType(), True),
                         StructField("state", StringType(), True),
                         StructField("country", StringType(), True)
                         ])

    headsDF = sparkSession.read\
                    .format("csv")\
                    .option("header", "false")\
                    .schema(headsSchema)\
                    .load("./datasets/heads.csv")

    joinDF = headsDF.join( fileStreamDF, ["city", "state", "country"] )

    # Registering Table
    # Create a view which can later be queried like a table
    joinDF.createOrReplaceTempView("SalesData")

    categoryDF = sparkSession.sql("SELECT city, regional_head, sales \
                                    FROM SalesData \
                                    WHERE state = 'California'")

    sales = categoryDF.groupBy("regional_head")\
                  .agg({"sales": "sum"})\
                  .withColumnRenamed("sum(sales)", "tot_sales")\
                  .orderBy("tot_sales", ascending=False)

    # Write out our dataframe to the console
    query = sales.writeStream\
                      .outputMode("complete")\
                      .format("console")\
                      .option("truncate", "false")\
                      .option("numRows", 30)\
                      .start()\
                      .awaitTermination()




