import utils.constant as constant
import os
from utils.qc_to_sqlserver import MEASURE
from dotenv import load_dotenv

load_dotenv()

try:
    influx_to_sqlserver = MEASURE(
        server=os.getenv('SERVER'),
        database=os.getenv('DATABASE'),
        user_login=os.getenv('USER_LOGIN'),
        password=os.getenv('PASSWORD'),
        table=os.getenv('DATA_TABLE'),
        table_columns=os.getenv('DATA_COLUMN'),
        table_log=os.getenv('TABLE_LOG'),
        table_columns_log=os.getenv('TABLE_COLUMNS_LOG'),
        influx_server=os.getenv('INFLUX_SERVER'),
        influx_database=os.getenv('INFLUX_DATABASE'),
        influx_user_login=os.getenv('INFLUX_USER_LOGIN'),
        influx_password=os.getenv('INFLUX_PASSWORD'),
        influx_columns=os.getenv('INFLUX_COLUMNS'),
        mqtt_topic=os.getenv('MQTT_TOPIC'),
        initial_db=os.getenv('INITIAL_DB')
    )

    influx_to_sqlserver.run()

except Exception as e:
    print(e)