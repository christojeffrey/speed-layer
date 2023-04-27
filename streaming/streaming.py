
# mock twitter api
# will post to kafka every 5 seconds

import time
import os
import requests
from kafka import KafkaProducer
from json import dumps
import ijson

# delay 15 seconds to wait for kafka to start
time.sleep(15)

DELAY = 1
URL = 'http://128.199.176.197:7551/streaming'
auth = 'Basic YTU3ZGUwODAtZjdiYy00MD'

# transfer encoding: chunked
headers = {'Authorization':'Basic YTU3ZGUwODAtZjdiYy00MDIyLTkzZGMtNjEyZDJhZjU4ZDMxOg==',
            'User-Agent':'PostmanRuntime/7.29.2',
            'Accept':'application/json',
            'Accept-Encoding':'gzip, deflate, br',
            'Connection':'keep-alive'}


session = requests.Session()
producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda x: dumps(x.decode()).encode('utf-8'))

def get_stream(URL):
    # use session to read each object from stream (not each line). then pass it to post_to_kafka
    currentObject = {}
    with session.get(URL, headers=headers, stream=True) as r:
        # use ijson to parse each object from stream
        parser = ijson.parse(r.raw)
        for prefix, event, value in parser:
            if (prefix, event) == ('item', 'start_map'):
                currentObject = {}
            elif (prefix, event) == ('item', 'end_map'):
                # print(currentObject)
                # pass to kafka as byte
                post_to_kafka(dumps(currentObject).encode('utf-8'))
            elif event == 'string':
                # possible improvement: handle nested prefix. like item.user.name (split by .)
                currentObject[prefix] = value
                # print("nambah")
          


          


def post_to_kafka(value):
    producer.send('streaming', value=value)
    # flush to make sure all messages are sent. forcing it to be synchronous
    producer.flush()
    # print("posted to kafka")

# do this forever
while True:
    try:
        get_stream(URL)
    except Exception as e:
        print(e)
        time.sleep(DELAY)