const config = require('./config');
var kafka = require('kafka-node');

var producer = null;
var readyFlag = false;

produceJob = function (topic, pload, isBatchProducer, callback) {
  getProducer(topic, pload, isBatchProducer);
  function send() {
    producer.send([
      { topic: topic, messages: JSON.stringify(pload) }
    ], function (err, data) {
      if (err) callback(err, null);
      else callback(null, data);
    });
  }

  if (readyFlag) {
    send();
  } else {
    setTimeout(send, 2000);
  }
};

getProducer = function (topic, pload, isBatchProducer) {
  if (producer) {
    return producer;
  } else {
    setConnectoConnection(topic, pload, isBatchProducer);

    producer.on('ready', function () {
      readyFlag = true;
    });
  }
}

setConnectoConnection = function (topic, pload, isBatchProducer) {
  var HighLevelProducer = kafka.HighLevelProducer;
  var client = new kafka.KafkaClient({ kafkaHost: config.kafka_server });

  if (isBatchProducer) {
    // var client = new kafka.Client('35.233.196.190:9092', 'producer-node',
    //   {}, {
    //     noAckBatchSize: 5000000, //5 MB
    //     noAckBatchAge: 5000 // 5 Sec
    //   });
    producer = new HighLevelProducer(client, { requireAcks: 0 });
  } else {
    producer = new HighLevelProducer(client);
  }

  producer.on('error', function (err) {
    console.log('error', err);
  });

  return producer;
};

produceJob(config.kafka_topic, 'sample', false, (err, data) => {
  err ? console.log(err) : console.log(data)
})