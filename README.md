reference:

- https://github.com/mvillarrealb/docker-spark-cluster

# setup

1. install docker and docker-compose
2. `npm install` first inside rest folder (volume listening doesn't work in windows 10. you don't need to do this if you're in linux)
3. run `docker-compose up` to start the cluster

optional: check if kafka got the data using this command
`/opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic twitter --consumer.config /opt/bitnami/kafka/config/consumer.properties --from-beginning`

4. run the command in spark

5. open spark terminal in docker using `docker exec -it spark-master bash`

6. run `$SPARK_HOME/bin/spark-submit --driver-class-path /opt/spark-apps/postgresql-42.6.0.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 --jars /opt/spark-apps/postgresql-42.6.0.jar  /opt/spark-apps/main.py`

7. example endpoint to hit `http://localhost:3000/results?start=2020-12-12 23:55&end=2020-12-12 23:55`

## note

- hot reload for rest doesn't work in windows
