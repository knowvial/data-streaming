from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
from ConfigParser import ConfigParser

configParser = ConfigParser.RawConfigParser()   
configFilePath = r'./config.cfg'
configParser.read(configFilePath)

access_token = configParser.get('twitter', 'access_token')
access_token_secret =  configParser.get('twitter', 'access_token_secret')
consumer_key =  configParser.get('twitter', 'consumer_key')
consumer_secret =  configParser.get('twitter', 'consumer_secret')
kafka_server = configParser.get('kafka', 'server')
kafka_topic = configParser.get('kafka', 'topic')

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages(kafka_topic, data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient()
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track="trump")