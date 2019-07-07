FROM strapdata/elassandra

ADD cassandra.yml /usr/app/cassandra.yml
ADD jmx_prometheus_javaagent-0.3.0.jar /usr/app/jmx_prometheus_javaagent-0.3.0.jar
RUN echo 'JVM_OPTS="$JVM_OPTS -javaagent:/usr/app/jmx_prometheus_javaagent-0.3.0.jar=6090:/usr/app/cassandra.yml"' >> /etc/cassandra/cassandra-env.sh
