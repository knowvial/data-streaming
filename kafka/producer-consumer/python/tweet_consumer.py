from kafka import KafkaConsumer
import json
import sys
import configparser

config = configparser.ConfigParser()
config.read(r'./config.cfg')

kafka_server = config.get('kafka', 'server')
kafka_topic = config.get('kafka', 'topic')

tweet_download_file = config.get('consumer_file', 'file_name')

fileHandle = open(tweet_download_file, "a+")

consumer = KafkaConsumer(bootstrap_servers=kafka_server, group_id='app1', auto_offset_reset='earliest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe([kafka_topic])
for message in consumer :
  try:
    msg = message.value.get("user","").get("name", "") + "\t" + message.value.get("created_at","") + "\t" + message.value.get("text", "") + "\t" + message.value.get("retweet_count","")
    fileHandle.write(msg)
  except:
    print("Unexpected error:", sys.exc_info()[0])
    pass


fileHandle.close()