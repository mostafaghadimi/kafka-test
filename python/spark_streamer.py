import random
import string

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pyspark_cassandra
from pyspark_cassandra import streaming
from datetime import datetime


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


# 1. install requirements.txt
# set up Spark and Cassandra
# 3. start the stream by:
#   spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0,TargetHolding/pyspark-cassandra:0.1.5 --conf spark.cassandra.connection.host=127.0.0.1 example.py my-topic

# dependent on Spark configuration
sc = SparkContext("spark://MASTER:7077", "streaming")
# set batch interval of 3 second
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
