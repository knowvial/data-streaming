from kafka import KafkaConsumer
from kafka import KafkaProducer
import json,time
from xlutils.copy import copy    
from xlrd import open_workbook
import pandas

consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
KafkaConsumer()
consumer.subscribe("test")

rowx=0
colx=0

for msg in consumer:
        book_ro = open_workbook("twitter.xls")
        book = copy(book_ro)  # creates a writeable copy
        sheet1 = book.get_sheet(0)  # get a first sheet
        sheet1.write(rowx,colx, msg[6])
        book.save("twitter.xls")
