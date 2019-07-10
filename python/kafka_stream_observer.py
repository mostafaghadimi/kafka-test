import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

sc = SparkContext(appName='KafkaSparkStream')
ssc = StreamingContext(sc, 60)

topic = "hossein"
broker = "kafka:9092"

# kafka_stream = KafkaUtils.createStream(ssc, "zookeeper:2181", 'test-consumer-group', {topic: 1},
#                                        {"metadata.broker.list": broker,
#                                        "auto.offset.reset": "smallest"})
kafka_stream = KafkaUtils.createDirectStream(ssc, [topic], {'metadata.broker.list': broker,
                                                            # 'server.bootstrap': zookeeper,
                                                            'auto.offset.reset': 'smallest'})
parsed = kafka_stream.map(lambda v: json.loads(v[1]))
parsed.count().map(lambda x: 'Messages in this batch: %s' % x).pprint()

ssc.start()
ssc.awaitTermination()
