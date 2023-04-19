# do batch read from kafka:9092 every 5 minutes, then insert into postgres

# imprt spark

from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, unix_timestamp
from pyspark.sql.types import TimestampType
import time
import json
import datetime



spark = SparkSession.builder.appName("spark batch app").getOrCreate()

# df = spark.read.format("kafka").option("kafka.bootstrap.servers", "kafka:9092").option("subscribe", "twitter").load()


# df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# df.show()

last_offset = 0
whole_data = []

answer = {}

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

            # add to answer. will round to 5 minutes. for example: 2020-01-01 00:00:01 -> 2020-01-01 00:00:00, 2020-01-01 00:00:06 -> 2020-01-01 00:00:05
            if social_media not in answer:
                answer[social_media] = {}

            # round down to 5 minutes
            # take the minute
            minute = int(created_time[14:16])
            # round down to 5 minutes
            minute = int(minute / 5) * 5
            # convert to string
            minute = str(minute)
            # add 0 if minute is 1 digit
            if len(minute) == 1:
                minute = "0" + minute

            # new created_time. zero in seconds and milliseconds
            created_time = created_time[0:14] + minute + ":00"
            print("new created_time")
            print(created_time)

            # add to answer
            if created_time not in answer[social_media]:
                answer[social_media][created_time] = {
                    "count": 0,
                    "created_at": created_time,
                    "updated_at": created_time,
                    "target_name": {}
                }
                # add target_name to answer
                # dictionary of target_name
                answer[social_media][created_time]["target_name"][target_name] = 1
            
            # increase count
            answer[social_media][created_time]["count"] += 1

            answer[social_media][created_time]["target_name"][target_name] = 1
            # update updated_at
            answer[social_media][created_time]["updated_at"] = created_time






        except Exception as e:
            print("failed to parse row value")
            print(e)
            continue
            
    # TODO: post to postgres
    # example of read
    # https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html

    jdbcDF = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/mydb") \
        .option("dbtable", "social_media_stats") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .load()
    jdbcDF.show(1)

    # social_media, timestamp, count, unique_count, created_at, updated_at
    # insert into postgres
    # https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html

    print("answer")
    print(answer)

    # delete all data, then insert
    # clear jdbcDF first
    jdbcDF = spark.createDataFrame([], jdbcDF.schema)
    # add data to jdbcDF
    for social_media in answer:
        for created_time in answer[social_media]:
            # add to jdbcDF
            unique_count = len(answer[social_media][created_time]["target_name"])
            # cast created_time to timestamp
            created_time_timestamp = datetime.datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S")
            created_at_timestamp = datetime.datetime.strptime(answer[social_media][created_time]["created_at"], "%Y-%m-%dT%H:%M:%S")
            updated_at_timestamp = datetime.datetime.strptime(answer[social_media][created_time]["updated_at"], "%Y-%m-%dT%H:%M:%S")

            data = [(social_media, 
                    created_time_timestamp,
                    answer[social_media][created_time]["count"],
                    unique_count,
                    created_at_timestamp,
                    updated_at_timestamp)]
            
            jdbcDF = jdbcDF.union(spark.createDataFrame(data, jdbcDF.schema))
    print("jdbcDF")
    jdbcDF.show(5)

    jdbcDF.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/mydb") \
        .option("dbtable", "social_media_stats") \
        .option("user", "postgres") \
        .option("password", "postgres") \
        .mode("overwrite") \
        .save()
    






    time.sleep(20)
