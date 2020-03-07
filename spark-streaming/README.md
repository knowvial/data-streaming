# Some basic 

## 1. Word Count with structured streaming

```
cd spark-streaming
```

Open two terminals. In one terminal
```
nc -p 9999 -l

or 

nc -lk 9999
```

In another terminal run the following comamnd
```
spark-submit word_count_nc.py localhost 9999
```
You should notice the table updating.