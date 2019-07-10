import json
# import time
# import datetime
# import requests
from kafka import KafkaProducer
# from sseclient import SSEClient as EventSource


while True:
    message = {'user': 'hossein', 'app_name': 'kafka_spark_test'}
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    producer.send('wednsday', value=json.dumps(message).encode('utf-8'))
    print('1 item sent')
