from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(bootstrap_servers="192.168.123.4:9094", client_id='test')

topic_list = [NewTopic(name="example_topic", num_partitions=1, replication_factor=3)]
admin_client.create_topics(new_topics=topic_list, validate_only=False)
