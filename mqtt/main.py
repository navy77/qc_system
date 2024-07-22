import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
from bson import ObjectId
import os
from dotenv import load_dotenv
#
load_dotenv()
# MongoDB 
username = os.getenv('USER_LOGIN')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
server = os.getenv('SERVER')
collection = os.getenv('COLLECTION')
port = int(os.getenv('MONGO_PORT'))
connection_string = f'mongodb://{username}:{password}@{server}:{port}/{database}?authSource=admin'

mqtt_broker = os.getenv('MQTT_BROKER')
mqtt_port = int(os.getenv('MQTT_PORT'))
mqtt_topic = os.getenv('MQTT_TOPIC')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("test/#")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    topic_rtn = f"{msg.topic}_rtn"
    spec_id = json.loads(msg.payload.decode()).get("spec_id")
    print(topic_rtn)
    print(spec_id)
    publish(client, topic_rtn,spec_id)

def query(data):
    client = MongoClient(connection_string)
    db = client[database]
    collection = db['spec']
    query = {"spec_id": data}
    result = collection.find_one(query)
    return result

def json_encoder(obj):
    if isinstance(obj,ObjectId):
        return str(obj)

def publish(client,topic,spec_id):
    topic = topic
    query_data = query(spec_id)
    print(query_data)
    json_data = json.dumps(query_data,default=json_encoder)

    client.publish(topic,json_data)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.enable_bridge_mode()

    client.connect(mqtt_broker, 1883, 60)

    client.loop_forever()

while True:
    main()