# Some basic
* [Streaming word count thorugh socket listner](#word-count-with-structured-streaming)
* [Streaming aggregation thorugh file listner](#word-count-with-structured-streaming)

## Word Count with structured streaming
In this exercise, Spark streaming will listen for a stream of words entered in a terminal.

```
cd spark-streaming
```

> On Windows, use Anconda powershell in Administrator mode to execute the following commands. Download windows specific Netcat utility.

Open two terminals. In one terminal to send a stream of messages on a certain port e.g. 9999
```
nc -p 9999 -l   (Debian 9 Linux)

or 

ncat -lk 9999   (Windows)
```

In another terminal run the following comamnd
```
spark-submit word_count_nc.py localhost 9999
```

Start sending messages in the first terminal. You should notice the table with word count displayed on the second terminal. As you enter more lines in the first terminal, you will notice spark streaming program computes the overall word count and displays the latest count as another new table as shown below.
```
-------------------------------------------
Batch: 1
-------------------------------------------
+----------+-----+
|      word|count|
+----------+-----+
|       you|    2|
|   people,|    1|
|     alarm|    1|
|     given|    1|
|     don’t|    1|
|       but|    1|
|  possible|    1|
|       You|    1|
|anything’s|    1|
|       the|    1|
|      want|    1|
|     seen,|    1|
|    spread|    1|
|     know,|    2|
|        to|    1|
|     we’ve|    1|
+----------+-----+
```

## Sales by state Aggregation
```
cd spark-streaming
```

> On Windows, use Anconda powershell in Administrator mode to execute the following commands. 

For this program we will use two files in "datasets" folder sales1.csv and sales2.csv. Each of these files have sales data for each 
product by country, state and city. Each file has 1000 entries. We would like to find the total sales by state. 

This streaming program waits for new files to arrive in folder "datasets/droplocation" folder. We want to simulate streaming by copying sales csv files one at a time to simulate the streaming application picks the new file content and computes the aggregation overall and displays on the console.

> Please make sure "datasets/droplocation" folder is empty everytime you run this program and copy one file (sales1.csv and sales2.csv) at a time to the "datasets/droplocation" folder.

In one terminal run the following comamnd
```
spark-submit sales_by_state.py
```
Now copy sales1.csv into "datasets/droplocation" folder.

You should notice a table like the following (you may have to wait few seconds to notice the table).
```
-------------------------------------------
Batch: 0
-------------------------------------------
+--------------------+---------+
|state               |tot_sales|
+--------------------+---------+
|California          |6461.0   |
|Texas               |5741.0   |
|Florida             |3646.0   |
|New York            |2830.0   |
|Pennsylvania        |1983.0   |
|Ohio                |1668.0   |
|Missouri            |1630.0   |
|Georgia             |1620.0   |
|Virginia            |1546.0   |
|District of Columbia|1529.0   |
|Colorado            |1353.0   |
|Illinois            |1252.0   |
```
Now add sales2.csv into  "datasets/droplocation" folder. It should now display newly computed numbers as shown below.
```
-------------------------------------------
Batch: 1
-------------------------------------------
+--------------------+---------+
|state               |tot_sales|
+--------------------+---------+
|California          |12008.0  |
|Texas               |11998.0  |
|Florida             |7214.0   |
|New York            |5588.0   |
|Pennsylvania        |4024.0   |
|Ohio                |3807.0   |
|Virginia            |3174.0   |
|Georgia             |2976.0   |
|District of Columbia|2882.0   |
|North Carolina      |2774.0   |
|Missouri            |2709.0   |
|Colorado            |2485.0   |
|Illinois            |2207.0   |
|Arizona             |2148.0   |
```
