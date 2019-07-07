from datetime import datetime
import random
import string

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import pyspark_cassandra
from pyspark_cassandra import streaming

# spark-submit
# --master local
# --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.1,anguenot:pyspark-cassandra:0.10.1
# ksc_streamer.py


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


# "spark://MASTER:7077"
conf = SparkConf() \
    .setAppName("Streaming test") \
    .set("spark.cassandra.connection.host", "localhost")
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 5)

topic = "test"
kafka_stream = KafkaUtils.createStream(ssc,
                                       # Zookeeper quorum (hostname:port,hostname:port,..)
                                       "localhost:9092",
                                       # group ID
                                       "topic",
                                       # topics with their corresponding partition
                                       {topic: 1})

raw = kafka_stream.flatMap(lambda x: [x])
time_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
# clean = raw.map(lambda xs: xs[1].split(","))

# Match cassandra table fields with dictionary keys
# this reads input of format: x[partition, timestamp]
my_row = raw.map(lambda x: {
    "testid": str(x),
    "date": random_string(),
    "time1": time_now,
    "time2": time_now
})

# save to cassandra
my_row.saveToCassandra("tutorialspoint", "test1")

ssc.start()  # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
