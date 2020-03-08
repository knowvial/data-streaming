# Some basic 

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

