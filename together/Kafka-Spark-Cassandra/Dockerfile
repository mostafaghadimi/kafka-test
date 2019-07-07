FROM wurstmeister/kafka
ADD prom-jmx-agent-config.yml /usr/app/prom-jmx-agent-config.yml
ADD jmx_prometheus_javaagent-0.10.jar /usr/app/jmx_prometheus_javaagent.jar
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
CMD ["/wait-for-it.sh", "zookeeper:2181", "--", "start-kafka.sh"]
