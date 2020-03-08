
# Kafka - Spark Streaming Example
In this lab has two parts
* One one side we will use Kafka producer [instructions](https://github.com/rbotla/data-streaming/tree/master/kafka/producer-consumer/python) to send tweets to a Kafka topic. 
* On the other side, we will run Kafka streaming program to get sentiment score for each tweet.

> On Windows, use Anconda powershell in Administrator mode to execute the following commands. 

> Ensure to update an appropriate "2.11:2.4.5" version in the follownig command. Check ```ls $SPARK_HOME/jars``` to see the version associated with the kafka jars. Note there is a ":" in the before the Spark version.


In the first terminal, Run the following command for Spark streaming to get the tweets from Kafka and process the tweets in real-time. This program accepts three arguments - Kafka Server, Port and the topic name from where tweets to be retrieved.
```
cd /spark-streaming/kafka
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 kafka_twitter.py localhost 9092 covid
```

In the second terminal, run the following command
```
cd kafka/consumer-producer/python
python3 tweet_producer.py
```

You should notice, Spark streaming computing and displaying sentiment score for each tweet. A positive score and negative scores indicate positive and negative sentiments for each tweet.

```
-------------------------------------------
Batch: 0
-------------------------------------------
+--------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
|tweet                                                                                                                                                   |sentiment_score|
+--------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
|"RT @RiRiLoLoArts1: Because good things that bring hope and make people less pressed to keep up with the news are bad for journalists https:\u2026"     |2.0            |
|"RT @RiRiLoLoArts1: Because good things that bring hope and make people less pressed to keep up with the news are bad for journalists"                  |2.0            |
|"RT @AndyRuther: If only people contracted the coronavirus for not using their turn signal."                                                            |0.0            |
|"RT @BrianKarem: I attended two gaggles today and saw what @realDonaldTrump said this morning. The admin.  continues to promote the false na\u2026"     |0.0            |
|"RT @PreetBharara: Is it just me or is Trump\u2019s lying crap about the Coronavirus infinitely less credible (and infinitely more dangerous) tha\u2026"|-5.0           |
|"RT @96fj_: Ngl coronavirus is overdoing it now"                                                                                                        |0.0            |
|"RT @goodmiad: I ain\u2019t gonna say it but you know what I\u2019m saying."                                                                            |0.0            |
|"RT @joshtpm: TPM: We're placing all COVID-19 related content outside our Prime paywall. https://t.co/4SzD9HOvc5 via @TPM"                              |0.0            |
|"RT @goodbeanalt: coronavirus rate drops to 0%"                                                                                                         |0.0            |
|"RT @ShaneGoldmacher: This is a headline from California\n\n\"Chaos at hospitals due to shortage of coronavirus tests\"\n\nhttps://t.co/TPtdR6Uoy5"     |-4.0           |
|"RT @politico: A meeting of European ambassadors set to take place Friday was canceled after Croatia\u2019s representative went into a precaution\u2026"|0.0            |
|"RT @TeaPainUSA: \"I like the numbers being where they are. I don't need to have the numbers double because of one ship\"  https://t.co/oiEJ6N\u2026"   |2.0            |
|"RT @RealJamesWoods: Exclusive: China's silence caused dangerous global coronavirus spread, says Gordon Chang /// And the porous borders in\u2026"      |0.0            |
|"You would think that doctors out of all people should know better."                                                                                    |2.0            |
|"RT @gtconway3d: no words https://t.co/bl7YNMMVHT"                                                                                                      |-1.0           |
|"Oh my....\n#coronavirus\n#CoronavirusOutbreak\n#CoronaVirusUpdates\n#coronavirusus\n#coronavirususa\n#COVID2019\u2026 https://t.co/vpKdoUQv3p"         |0.0            |
|"RT @saintdiabIo: Performers at Coachella while there\u2019s a coronavirus outbreak in the crowd  https://t.co/HhjXPdornb"                              |-2.0           |
|"RT @AndyBiotech: #COVID19 Things start getting crazy out there...\n\nCDC should really start thinking about building those drive-in testing c\u2026"   |-2.0           |
|"RT @Neurophysik: This person Biswaroop Roy Chowdhury's video is very viral on YouTube and Facebook. It is full of misinformation on Coronav\u2026"     |-2.0           |
|"RT @MattBarrie: I mean. If anyone could kill a virus..."                                                                                               |-3.0           |
+--------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+
only showing top 20 rows
```

Reference - https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html
