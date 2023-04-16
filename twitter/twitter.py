
# mock twitter api
# will post to kafka every 5 seconds

import time
import os
from kafka import KafkaProducer
DELAY = 1

# add 15 seconds delay to wait for kafka to start
time.sleep(15)


count = 0
def get_tweets():
    global count
    count += 1
    return "hello world second:" + str(count)

def post_to_kafka(tweets):
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    # tweet as bytes
    producer.send('twitter', tweets.encode('utf-8'))
    # flush to make sure all messages are sent. forcing it to be synchronous
    producer.flush()
    print("posted to kafka")


while True:
    tweets = get_tweets()
    post_to_kafka(tweets)
    time.sleep(DELAY)