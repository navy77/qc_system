import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
import pymssql

# Load environment variables
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
    else:
        print("Payload is not a dictionary")

def query(part_no, process):
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table} WHERE part_no = '{part_no}' and process = '{process}'"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except pymssql.Error as e:
        print(f"Error querying MSSQL: {e}")
        return None
    finally:
        conn.close()
    
    field_names = ['spec_id', 'process', 'part_no', 'item_no', 'item_check', 'spec_nominal', 'tolerance_max', 'tolerance_min', 'point', 'method']
    dict_data = [dict(zip(field_names, item)) for item in results]
    json_data = json.dumps(dict_data, indent=4)

    return json_data

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
