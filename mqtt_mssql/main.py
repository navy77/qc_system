import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
import pymssql
import pandas as pd

load_dotenv()

username = os.getenv('USER_LOGIN')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
server = os.getenv('SERVER')
table = os.getenv('TABLE')

mqtt_broker = os.getenv('MQTT_BROKER')
mqtt_port = int(os.getenv('MQTT_PORT'))
mqtt_topic = os.getenv('MQTT_TOPIC')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    topic_rtn = f"{msg.topic}_rtn"
    payload = json.loads(msg.payload.decode())

    if isinstance(payload, dict):
        spec_id = payload.get("spec_id")
        if spec_id:
            publish(client, topic_rtn, spec_id)


def query(part_no, process):
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        cursor = conn.cursor(as_dict=True)

        query = f"SELECT * FROM {table} WHERE part_no = '{part_no}' and process = '{process}'"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        if results:
            df = pd.DataFrame(results)
            df['part_no_item'] = df['part_no']+"-"+df['item_no'].astype(str)
            df = df.loc[df.groupby('part_no_item')['rev'].idxmax()]
            df.drop(columns=['part_no_item','register','rev'],inplace=True)
            json_data = df.to_json(orient='records')
            return json_data
    except pymssql.Error as e:
        print(f"Error querying MSSQL: {e}")
        return None

def publish(client, topic, spec_id):
    part_no, process = spec_id.split('_')
    query_data = query(part_no, process)

    if query_data:
        client.publish(topic, query_data)
    else:
        print(f"No data found for spec_id: {spec_id}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
