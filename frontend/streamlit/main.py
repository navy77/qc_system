import streamlit as st
import dotenv
import pymssql
import os
import pandas as pd
from influxdb import InfluxDBClient
from datetime import datetime

def preview_sqlserver(server, user_login, password, database, table):
    try:
        cnxn = pymssql.connect(server, user_login, password, database)
        cursor = cnxn.cursor(as_dict=True)
        
        cursor.execute(f'SELECT * FROM {table}')
        data = cursor.fetchall()
        cursor.close()
        cnxn.close()

        if data:
            df = pd.DataFrame(data)
            df['part_no_item'] = df['part_no']+"-"+df['item_no'].astype(str)
            df = df.loc[df.groupby('part_no_item')['rev'].idxmax()]
            df.drop(columns=['part_no_item'],inplace=True)
            for col in df.columns:
                if df[col].dtype == 'object': 
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except ValueError:
                        pass 
                elif pd.api.types.is_datetime64_any_dtype(df[col]):  # register columns
                    try:
                        df[col] = pd.to_datetime(df[col])
                    except Exception:
                        pass 
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.error('Error: SQL Server returned no data', icon="❌")
    except Exception as e:
        st.error(f'Error: {str(e)}', icon="❌")
    st.markdown("---")

def preview_influx(st,influx_server,influx_user_login,influx_password,influx_database,column_names,mqtt_topic) :
      try:
            result_lists = []
            client = InfluxDBClient(influx_server, 8086,influx_user_login,influx_password,influx_database)
            # print(mqtt_topic.split('/')[0])
            # if mqtt_topic.split('/')[0] =='data':
            query = f"select * from mqtt_consumer where topic = '{mqtt_topic}' order by time desc limit 5"
            result = client.query(query)
            if list(result):
                query_list = list(result)[0]
                df = pd.DataFrame(query_list)
                df.time = pd.to_datetime(df.time).dt.tz_convert('Asia/Bangkok')
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.error('Error: influx no data', icon="❌")

      except Exception as e:
          st.error('Error: '+str(e), icon="❌")

def conn_sql(st,server,user_login,password,database):
        try:
            cnxn = pymssql.connect(server,user_login,password,database)
            st.success('SQLSERVER CONNECTED!', icon="✅")
            cnxn.close()
        except Exception as e:
            st.error('Error,Cannot connect sql server :'+str(e), icon="❌")

def config_db_connect(env_headers):
    if env_headers == "SQLSERVER":
        form_name = "config_db_connect_sql"
    elif env_headers == "INFLUXDB":
        form_name = "config_db_connect_influx"

    with st.form(form_name):

        total_env_list = None
        if env_headers == "SQLSERVER":
            total_env_list = sql_server_env_lists = ["SERVER","DATABASE","USER_LOGIN","PASSWORD"]
        elif env_headers == "INFLUXDB":
            total_env_list = influxdb_env_lists = ["INFLUX_SERVER","INFLUX_DATABASE","INFLUX_USER_LOGIN","INFLUX_PASSWORD"]
        else :
            st.error("don't have the connection")

        if total_env_list is not None:
            st.header(env_headers)
            cols = st.columns(len(total_env_list))
            for j in range(len(total_env_list)):
                param = total_env_list[j]
                if "PASSWORD" in param or "TOKEN" in param:
                    type_value = "password"
                else:
                    type_value = "default"
                os.environ[param] = cols[j].text_input(param,os.environ[param],type=type_value)
                dotenv.set_key(dotenv_file,param,os.environ[param])

            cols = st.columns(2) 

            if env_headers == "SQLSERVER":

                sql_check_but = cols[0].form_submit_button("CONECTION CHECK")
                if sql_check_but:
                    conn_sql(st,os.environ["SERVER"],os.environ["USER_LOGIN"],os.environ["PASSWORD"],os.environ["DATABASE"])

            elif env_headers == "INFLUXDB":
                influx_check_but = cols[0].form_submit_button("CONECTION CHECK")
                if influx_check_but:
                    try:
                        client = InfluxDBClient(os.environ["INFLUX_SERVER"], 8086, os.environ["INFLUX_USER_LOGIN"], os.environ["INFLUX_PASSWORD"], os.environ["INFLUX_DATABASE"])
                        result = client.query('select * from mqtt_consumer order by time limit 1')
                        st.success('INFLUXDB CONNECTED!', icon="✅")
                    except Exception as e:
                        st.error("Error :"+str(e))
            else:
                st.error('Dont have the connection!', icon="❌")

    st.markdown("---")

def get_db_connection():
    conn = pymssql.connect(
        server= os.environ["SERVER"],
        user=os.environ["USER_LOGIN"],
        password=os.environ["PASSWORD"],
        database=os.environ["DATABASE"]
    )
    return conn

def insert_to_db(spec_id,part_no,rev, process, item_no, item_check, spec_nominal, tolerance_max, tolerance_min, method, point,register):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO master_spec (spec_id,part_no,rev,process, item_no, item_check, spec_nominal, tolerance_max, tolerance_min, method, point,register) 
            VALUES (%s,%s,%d,%s,%d,%s,%d,%s,%s,%d,%d,%s)
            """,
            (spec_id,part_no,rev,process,item_no, item_check, spec_nominal, tolerance_max, tolerance_min, method, point,register)
        )
        conn.commit()
        st.success("Data inserted successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def config_master_spec():
    col1,col2,col3 = st.columns(3)
    with col2:
        with st.form("master_spec_form",clear_on_submit=False):
            st.markdown("""<h3 style='text-align: center;'>Master Configulation</h3>""", unsafe_allow_html=True)
            part_no = st.text_input("part_no").upper()
            rev = st.number_input("rev",step=1,min_value=1)
            process = st.text_input("process")
            item_no = st.number_input("item_no", min_value=1)
            item_check = st.text_input("item_check").upper()
            spec_nominal = st.number_input("spec_nominal",step=0.001,format="%0.3f")
            tolerance_max = st.number_input("tolerance_max",step=0.001,format="%0.3f")
            tolerance_min = st.number_input("tolerance_min",step=0.001,format="%0.3f")
            method = st.number_input("method",min_value=1)
            point = st.number_input("point",min_value=1)
            # Submit button
            button_col1, button_col2, button_col3 = st.columns([0.7, 0.2, 0.2])     
            with button_col3:
                submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                register = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                spec_id = str(part_no)+"-"+str(process)+"-"+str(item_no)+"-"+str(rev)
                insert_to_db(spec_id,part_no,rev, process, item_no, item_check, spec_nominal, tolerance_max, tolerance_min, method, point, register)
                

def main_layout():
    st.set_page_config(
            page_title="QC System",
            page_icon="💻",
            layout="wide",
            initial_sidebar_state="expanded",
        )
    st.markdown("""<h1 style='text-align: center;'>QC MONITORING SYSTEM</h1>""", unsafe_allow_html=True)

    text_input_container = st.empty()
    password = text_input_container.text_input("Input password", type="password")

    if password == "1":
        text_input_container.empty()
        tab1, tab2,tab3,tab4  = st.tabs(["📝 Dashboard", "⚙️ Project Configulation","🔑 DB Connection","🔍 Data Preview"])
        
        with tab1:
            st.write("Monitor data")
        with tab2:
            st.write("Master Configulation")
            config_master_spec()
        with tab3:
            st.write("DB Connection")
            config_db_connect("SQLSERVER")
            config_db_connect("INFLUXDB")
        with tab4:
            st.write("MSSQL Data Preview")
            preview_sqlserver(os.environ["SERVER"],os.environ["USER_LOGIN"],os.environ["PASSWORD"],os.environ["DATABASE"],os.environ["SQL_TABLE"])
            st.write("INFLUX Data Preview")
            preview_influx(st,os.environ["INFLUX_SERVER"],os.environ["INFLUX_USER_LOGIN"],os.environ["INFLUX_PASSWORD"],os.environ["INFLUX_DATABASE"],os.environ["INFLUX_COLUMN"],os.environ["MQTT_TOPIC"])

    elif password == "":
        pass
    else:
        st.toast('PASSWORD NOT CORRECT!', icon='❌')

if __name__ == "__main__":
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    main_layout()