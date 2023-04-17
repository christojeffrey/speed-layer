# import requests

# url = 'https://www.googleapis.com/qpxExpress/v1/trips/search?key=mykeyhere'
# payload = open("request.json")
# headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
# r = requests.post(url, data=payload, headers=headers)

from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(\
    "my_topic",\
    bootstrap_servers=['localhost:9092'],\
    auto_offset_reset='earliest',\
    enable_auto_commit=True,\
    group_id='my-group',\
    value_deserializer=lambda x: loads(x.decode('utf-8'))\
)

for message in consumer:
    message = message.value
    print(message)