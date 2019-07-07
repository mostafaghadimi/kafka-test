from _datetime import datetime
import os
import random
import string

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

os.environ['PYSPARK_SUBMIT_ARGS'] = '--conf spark.ui.port=4040 --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.1,anguenot:pyspark-cassandra:0.10.1'


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


# or for master: "spark://MASTER:7077"
conf = SparkConf() \
    .setAppName("Streaming test") \
    .setMaster("local[2]") \
    .set("spark.cassandra.connection.host", "127.0.0.1")
sc = SparkContext(conf=conf)

ssc = StreamingContext(sc, 3)

# name of our topic, I guess it was "test"
topic = "test"

kafkaStream = KafkaUtils.createStream(ssc,
                                      # Zookeeper quorum (hostname:port,hostname:port,..)
                                      "localhost:9092",
                                      # group ID
                                      "topic",
                                      # topics with their corresponding partition
                                      {topic: 1})

raw = kafkaStream.flatMap(lambda kafkaS: [kafkaS])
time_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
# clean = raw.map(lambda xs: xs[1].split(","))

# Match cassandra table fields with dictionary keys
# this reads input of format: x[partition, timestamp]
my_row = raw.map(lambda x: {
      "testid": str(x),
      "date": randomString(),
      "time1": time_now,
      "time2": time_now
})

# save to cassandra
my_row.saveToCassandra("tutorialspoint", "test1")

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
