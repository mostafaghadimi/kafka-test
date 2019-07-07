import json
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

conf = SparkConf() \
    .setAppName("Streaming test") \
    .set("spark.cassandra.connection.host", "localhost")

sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 5)

topic = "test"
broker = "localhost:9092"

kafka_stream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": broker})
# lines = kvs.map(lambda x: x[1])
# counts = lines.flatMap(lambda line: line.split(" ")) \
#               .map(lambda word: (word, 1)) \
#               .reduceByKey(lambda a, b: a+b)
#
# counts.pprint()
parsed = kafka_stream.map(lambda v: json.loads(v[1]))
parsed.count().map(lambda x: 'messages in this batch: %s' % x).pprint()
server_urls = parsed.map(lambda message: message['server_url'])

server_url_counts = server_urls.countByValue()
server_url_counts.pprint()

ssc.start()
ssc.awaitTermination()
