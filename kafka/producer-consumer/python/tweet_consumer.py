from kafka import KafkaConsumer
import json,time
import configparser

config = configparser.ConfigParser()
config.read(r'./config.cfg')

kafka_server = config.get('kafka', 'server')
kafka_topic = config.get('kafka', 'topic')

tweet_download_file = config.get('consumer_file', 'file_name')

fileHandle = open(tweet_download_file, "a+")

consumer = KafkaConsumer(bootstrap_servers=kafka_server, auto_offset_reset='latest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe([kafka_topic])
for message in consumer :
  fileHandle.write(message.text)

fileHandle.close()