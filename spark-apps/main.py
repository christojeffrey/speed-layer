# do batch read from kafka:9092 every 5 minutes, then insert into postgres

# imprt spark
from pyspark.sql import SparkSession
import time
import json



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
# key, value, topic, partition, offset, timestamp, timestampType
    df = df.selectExpr("CAST(value AS STRING)", "CAST(topic AS STRING)", "CAST(partition AS STRING)", "CAST(offset AS STRING)", "CAST(timestamp AS STRING)", "CAST(timestampType AS STRING)")
    # show the first row
    df.show(1)

    # process
    result = df.collect()
    answer = {}
    # target - insert into postgres (social_media, timestamp, count, unique_count, created_at, updated_at)
    print("result:")
    for row in result:
        try:
            # parse row value as dict
            rowValue = eval(row.value)
            print("rowValue")
            # print typeof rowValue
            print(type(rowValue))
            # parse str to dict
            rowValue = json.loads(rowValue)
            print(type(rowValue))
            # set as dict
            # get social media with key crawler_target.specific_resource_type
            social_media = rowValue['item.crawler_target.specific_resource_type']
            print("social_media")
            print(social_media)

            created_time = rowValue['item.created_time']
            print("item.created_time")
            print(created_time)

            target_name = rowValue['item.crawler_target.target_name']
            print("item.crawler_target.target_name")
            print(target_name)

        except Exception as e:
            print("failed to parse row value")
            print(e)
            continue
            
        # TODO: post to postgres
        # temporary, try to read database db table social_media_stats to check if postgres is working


        # url = 'postgresql://postgres:5432/mydb'
        # properties = {'user': 'postgres', 'password': 'postgres'}
        # df = spark.read.jdbc(url=url, table='social_media_stats', properties=properties)
        # df.show(1)
        jdbcDF = spark.read \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/mydb") \
            .option("dbtable", "social_media_stats") \
            .option("user", "postgres") \
            .option("password", "postgres") \
            .load()
        jdbcDF.show(1)





    time.sleep(20)
