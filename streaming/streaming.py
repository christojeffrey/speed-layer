
# mock twitter api
# will post to kafka every 5 seconds

import time
import os
import requests
from kafka import KafkaProducer
from json import dumps


DELAY = 1
URL = 'http://128.199.176.197:7551/streaming'
auth = 'Basic YTU3ZGUwODAtZjdiYy00MD'

headers = {'Authorization':'Basic YTU3ZGUwODAtZjdiYy00MDIyLTkzZGMtNjEyZDJhZjU4ZDMxOg==',
            'User-Agent':'PostmanRuntime/7.29.2',
            'Accept':'application/json',
            'Accept-Encoding':'gzip, deflate, br',
            'Connection':'keep-alive'}


# add 15 seconds delay to wait for kafka to start
time.sleep(15)


session = requests.Session()
producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda x: dumps(x.decode()).encode('utf-8'))

def get_stream(URL):
    with session.get(URL, headers=headers, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                post_to_kafka(line)

def post_to_kafka(value):
    producer.send('streaming', value=value)
    # flush to make sure all messages are sent. forcing it to be synchronous
    producer.flush()
    # print("posted to kafka")

get_stream(URL)