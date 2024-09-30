import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
import requests
import pandas as pd
import datetime

load_dotenv()

mqtt_broker = os.getenv('MQTT_BROKER')
mqtt_port = int(os.getenv('MQTT_PORT'))
mqtt_topic = os.getenv('MQTT_TOPIC')

url = os.getenv('URL')
cert_path = os.getenv('CERT_PATH')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    payload["time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(payload)
    # response = requests.post(url, json=payload, verify=cert_path)
    # if response.status_code == 201:
    #     print('Request was successful.')
    #     print('Response:', response.json())
    # else:
    #     print(f'Failed with status code: {response.status_code}')
    #     print('Response:', response.text)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
