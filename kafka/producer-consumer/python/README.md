# Kafka Producer and Consumer in Python

![Kafka Twitter](kafka-consumer-twitter.png)

[[_TOC_]]

## Instructions on Linux - Debian 9 
```
sudo apt update
sudo apt install python3-pip
pip3 --version
```

Install required libraries
```
pip3 install kafka
pip3 install kafka-python
pip3 install python-twitter
pip3 install tweepy
pip3 install configparser
```

Create a Kafka topic called covid
```
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic covid
```

Run Kafka consumer on CLI to watch for the tweets
```
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic covid --group app1
```

```
cd kafka/consumer-producer/python
```
Update your Twitter developer app credentials in config.cfg file. Refer to https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/

Run the twitter kafka producer program. CTRL + C to stop streaming after few seconds.
```
python3 tweet_producer.py
```

Check how many tweets are in the topic by partition
```
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group app1
```
---
Run Consumer program to read messages from Kafka and write to file
```
python3 tweet_consumer.py
```
---

Now, update tweet_consumer.py to write to HDFS. Hint: https://creativedata.atlassian.net/wiki/spaces/SAP/pages/61177860/Python+-+Read+Write+files+from+HDFS

## Instructions on Windows

Install Anaconda by following instructions on https://docs.anaconda.com/anaconda/install/windows/.

> On windows, execute all the following commands in Anaconda Powershell as an Administrator (preferable since some people seem to have issues on a normal command terminal). Also note, in some cases if you have only python version installed on your machine, you could use pip instead of pip3 in the following commands.

Install required libraries
```
pip3 install kafka
pip3 install kafka-python
pip3 install python-twitter
pip3 install tweepy
pip3 install configparser
```

Create a Kafka topic called covid
```
bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic covid
```

Run Kafka consumer on CLI to watch for the tweets
```
bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic covid --group app1
```

```
cd kafka\consumer-producer\python
```
Update your Twitter developer app credentials in config.cfg file. Refer to https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/

Run the twitter kafka producer program. CTRL + C to stop streaming after few seconds.
```
python3 tweet_producer.py
```

Check how many tweets are in the topic by partition
```
bin\windows\kafka-consumer-groups.bat --bootstrap-server localhost:9092 --describe --group app1
```
---
Run Consumer program to read messages from Kafka and write to file
```
python3 tweet_consumer.py
```
---