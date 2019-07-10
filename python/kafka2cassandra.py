# sample json:
# {"employee": {"name": "hossein", "salary": 56000, "married": true}}
import sys
from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster

consumer = KafkaConsumer('hossein', bootstrap_servers="kafka:9092")

cluster = Cluster(['localhost'])
session = cluster.connect('kafkacassandra')

# start the loop
try:
    print("hello!!!!!!!!!")
    for message in consumer:
        print(message)
        # entry = json.loads(json.loads(message.value))['log']
        entry = json.loads(message.value)
        # or
        # entry = json.loads(message)['employee'] if you're lazy.
        print(entry)
        print(type(entry))
        # parsed = json.loads(message[1])
        # print(parsed)
        # print(type(parsed))
        print("Entry name: {} salary: {} married: {}".format(
            entry['employee']['name'],
            entry['employee']['salary'],
            entry['employee']['married']))
        print("--------------------------------------------------")
        # use %s for everuthing!
        session.execute(
            """
                INSERT INTO employee (name, salary, married)
                VALUES (%s, %s, %s)
            """,
            (entry['employee']['name'],
             entry['employee']['salary'],
             entry['employee']['married']))
except KeyboardInterrupt:
    sys.exit()
