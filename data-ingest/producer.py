from time import sleep
from json import dumps
from kafka import KafkaProducer
import requests

url = 'http://128.199.176.197:7551/streaming'
auth = 'Basic YTU3ZGUwODAtZjdiYy00MD'

headers = {'Authorization':'Basic YTU3ZGUwODAtZjdiYy00MDIyLTkzZGMtNjEyZDJhZjU4ZDMxOg==',
            'User-Agent':'PostmanRuntime/7.29.2',
            'Accept':'application/json',
            'Accept-Encoding':'gzip, deflate, br',
            'Connection':'keep-alive'}

def get_stream(url):
    producer = KafkaProducer(\
        bootstrap_servers=['localhost:9092'],\
        value_serializer=lambda x: dumps(x.decode()).encode('utf-8')\
    )

    session = requests.Session()

    with session.get(url, headers=headers, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                producer.send('my_topic', value=line)

get_stream(url)


