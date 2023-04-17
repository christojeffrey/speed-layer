# do batch read from kafka:9092 every 5 minutes, then insert into postgres

# imprt spark
from pyspark.sql import SparkSession
import time
spark = SparkSession.builder.appName("spark batch app").getOrCreate()


# df = spark.read.format("kafka").option("kafka.bootstrap.servers", "kafka:9092").option("subscribe", "twitter").load()


# df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# df.show()

last_offset = 0
whole_data = []
while True:
    # only show data that have been read from kafka
    df = spark.read.format("kafka").option("kafka.bootstrap.servers", "kafka:9092").option("subscribe", "streaming").option("startingOffsets", """{"streaming":{"0":%s}}""" % last_offset).load()
    
    last_offset += df.count()
    print("last offset: ", last_offset)

    # value_deserializer=lambda x: loads(x.decode('utf-8'))

    df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    df.show()
    time.sleep(5)
