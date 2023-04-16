reference:

- https://github.com/mvillarrealb/docker-spark-cluster

check if kafka got the data using this command
`/opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic twitter --consumer.config /opt/bitnami/kafka/config/consumer.properties --from-beginning`

how to run in spark

first, install kafka using
`pip install kafka-python`

then, run the spark job using
`$SPARK_HOME/bin/spark-submit /opt/spark-apps/main.py`

need certain package, so use this to run the spark job with the package
`$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 /opt/spark-apps/main.py`
