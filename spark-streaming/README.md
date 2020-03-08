# Some basic 

## 1. Word Count with structured streaming
In this exercise, Spark streaming will listen for a stream of words entered in a terminal.

```
cd spark-streaming
```

Open two terminals. In one terminal
```
nc -p 9999 -l   (Debian 9 Linux)

or 

ncat -lk 9999   (Windows)
```

In another terminal run the following comamnd
```
spark-submit word_count_nc.py localhost 9999
```
