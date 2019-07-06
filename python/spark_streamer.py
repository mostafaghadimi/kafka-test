from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pyspark_cassandra
from pyspark_cassandra import streaming
from datetime import datetime

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
clean = raw.map(lambda xs: xs[1].split(","))

# Match cassandra table fields with dictionary keys
# this reads input of format: x[partition, timestamp]
my_row = clean.map(lambda x: {
      "testid": "test",
      "time1": x[1],
      "time2": time_now,
      "delta": (datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S.%f') -
       datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')).microseconds,
      })

# save to cassandra
my_row.saveToCassandra("KEYSPACE", "TABLE_NAME")

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
