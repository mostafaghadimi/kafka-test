# sample json:
# {"employee": {"name": "hossein", "salary": 56000, "married": true}}
import sys
from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster
from kafka.errors import NoBrokersAvailable

hosts = [
    '192.168.123.4:9094',   # master
    '192.168.123.25:9094',  # slave1
    '192.168.123.24:9094',  # slave2
]

topic_name = 'test'

for i in range(len(hosts)):
    try:
        consumer = KafkaConsumer(topic_name, bootstrap_servers=hosts[i])
    except NoBrokersAvailable:
        if i == len(hosts) - 1:
            raise
        print('broker #', (i + 1), 'is not available')
    else:
        break

cluster = Cluster(['localhost'])
session = cluster.connect('kafkacassandra')

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
