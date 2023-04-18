reference:

- https://github.com/mvillarrealb/docker-spark-cluster

check if kafka got the data using this command
`/opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic twitter --consumer.config /opt/bitnami/kafka/config/consumer.properties --from-beginning`

how to run in spark

open spark terminal in docker using
`docker exec -it spark-master bash`

`$SPARK_HOME/bin/spark-submit --driver-class-path /opt/spark-apps/postgresql-42.6.0.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 --jars /opt/spark-apps/postgresql-42.6.0.jar  /opt/spark-apps/main.py`

example endpoint to hit
`http://localhost:3000/results?start=2020-12-12 23:55&end=2020-12-12 23:55`
