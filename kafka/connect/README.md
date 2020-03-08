# Kafka Connect
![Kafka Connect Data Flow](kafka-connect.png)

<!--ts-->
* [Linux - Debian 9](#instructions-on-linux---debian-9)
* [Windows](#instructions-on-windows)
<!--te-->

## Instructions on Linux - Debian 9
Download jar files from https://github.com/jcustenborder/kafka-connect-twitter/releases.

```
cd kafka/connect

curl -sL https://github.com/jcustenborder/kafka-connect-twitter/releases/download/0.2.26/kafka-connect-twitter-0.2.26.tar.gz -o kafka-connect-twitter.tar.gz

tar -zxf kafka-connect-twitter.tar.gz
```

Confirm all the required jar files are located at usr/share/kafka-connect/kafka-connect-twitter location.

Ensure "plugins.path" location in connect-standalone.properties file is pointing to usr/share/kafka-connect (or equivalent on your machine). 

Enter Twitter developer credentials in twitter.properties file and update your search terms.

Create topics
```
kafka-topics.sh --zookeeper 127.0.0.1:2181 --create --topic twitter_status_connect --partitions 3 --replication-factor 1
kafka-topics.sh --zookeeper 127.0.0.1:2181 --create --topic twitter_delete_connect --partitions 3 --replication-factor 1
```

Start CLI consumer 
```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic twitter_status_connect --group app2
```

Run Connect and check if you can see the twitter results in the consumer CLI window.
```
connect-standalone.sh connect-standalone.properties twitter.properties
```


## Instructions on Windows
Download jar files from https://github.com/jcustenborder/kafka-connect-twitter/releases.

```
cd [REPO_HOME]\kafka\connect

Download https://github.com/jcustenborder/kafka-connect-twitter/releases/download/0.2.26/kafka-connect-twitter-0.2.26.tar.gz

Run the following command to untar the file
tar -zxf kafka-connect-twitter.tar.gz
```
You should see a "usr" folder created after you untar. Confirm all the required jar files are located at usr\share\kafka-connect\kafka-connect-twitter location.

Edit connect-standalone.properties file to ensure "plugins.path" parameter is pointing to usr\share\kafka-connect (or equivalent on your machine). Note: don't include "kafka-connect-twitter" in the path.

Enter Twitter developer credentials in twitter.properties file and update your search terms.

Create two topics that the Twitter Connector expects you to create.
```
bin\windows\kafka-topics.bat --zookeeper 127.0.0.1:2181 --create --topic twitter_status_connect --partitions 3 --replication-factor 1
bin\windows\kafka-topics.bat --zookeeper 127.0.0.1:2181 --create --topic twitter_delete_connect --partitions 3 --replication-factor 1
```

Start CLI consumer to view all tweets that connector will write to a Kafka topic.
```
bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic twitter_status_connect --group app2
```

Run Connect and check if you can see the twitter results in the consumer CLI window.
```
bin\windows\connect-standalone.bat connect-standalone.properties twitter.properties
```