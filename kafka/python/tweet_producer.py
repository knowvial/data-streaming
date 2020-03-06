from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
import configparser

config = configparser.ConfigParser()
config.read(r'./config.cfg')

access_token = config.get('twitter', 'access_token')
access_token_secret =  config.get('twitter', 'access_token_secret')
consumer_key =  config.get('twitter', 'consumer_key')
consumer_secret =  config.get('twitter', 'consumer_secret')
kafka_server = config.get('kafka', 'server')
kafka_topic = config.get('kafka', 'topic')

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages(kafka_topic, data.encode('utf-8'))
        print (data)
        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient(hosts= kafka_server)
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track=["coronavirus", "covid-19", "2019-nCoV", "SARS-CoV-2"])