import os
from pathlib import Path
from dotenv import load_dotenv
from utils.qc import MEASURE
try:
    env_path = Path('.env')
    load_dotenv(dotenv_path=env_path,override=True)
    qc_to_sqlserver = MEASURE(
        server=os.getenv('SERVER'),
        database=os.getenv('DATABASE'),
        user_login=os.getenv('USER_LOGIN'),
        password=os.getenv('PASSWORD'),
        table=os.getenv('TABLE'),
        table_columns=os.getenv('QC_COLUMN_NAMES'),
        table_log=os.getenv('TABLE_LOG'),
        table_columns_log=os.getenv('QC_TABLE_COLUMNS_LOG'),
        influx_server=os.getenv('INFLUX_SERVER'),
        influx_database=os.getenv('INFLUX_DATABASE'),
        influx_user_login=os.getenv('INFLUX_USER_LOGIN'),
        influx_password=os.getenv('INFLUX_PASSWORD'),
        influx_port=os.getenv('INFLUX_PORT'),
        column_names=os.getenv('MCSTATUS_TABLE_COLUMNS'),
        mqtt_topic=os.getenv('MQTT_TOPIC'),
        initial_db=os.getenv('INIT_DB'))
    qc_to_sqlserver.run()

except Exception as e:
    print(e)