import streamlit as st
import dotenv
import pymssql
import os
import pandas as pd
from influxdb import InfluxDBClient
from datetime import datetime
import altair as alt
import qrcode
import io

def preview_master_sqlserver(server, user_login, password, database, table):
    try:
        cnxn = pymssql.connect(server, user_login, password, database)
        cursor = cnxn.cursor(as_dict=True)
        cursor.execute(f'''SELECT TOP(5) * FROM {table}  order by register desc''')
        data = cursor.fetchall()
        cursor.close()
        cnxn.close()
        if data:
            df = pd.DataFrame(data)
            df = df.drop_duplicates(subset=['item_check'],keep='first')
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

def preview_production_sqlserver(server,user_login,password,database,table,spec_id):
        #connect to db
        cnxn = pymssql.connect(server,user_login,password,database)
        cursor = cnxn.cursor(as_dict=True)
        # create table
        try:
            cursor.execute(f'''SELECT TOP(5) * FROM {table} where spec_id = '{spec_id}'  order by register desc''')
            data=cursor.fetchall()
            cursor.close()
            if len(data) != 0:
                df=pd.DataFrame(data)
                st.dataframe(df,width=1500)
            else:
                st.error('Error: SQL SERVER NO DATA', icon="❌")
        except Exception as e:
            st.error('Error'+str(e), icon="❌")

def preview_influx(st,influx_server,influx_port,influx_user_login,influx_password,influx_database,column_names,spec_id) :
      try:
            client = InfluxDBClient(influx_server,influx_port,influx_user_login,influx_password,influx_database)

            query = f"SELECT time, topic, {column_names} FROM mqtt_consumer WHERE spec_id = '{spec_id}' AND topic !~ /_rtn/ order by time desc limit 5"

            result = client.query(query)
            if list(result):
                query_list = list(result)[0]
                df = pd.DataFrame(query_list)

                df.time = pd.to_datetime(df.time).dt.tz_convert('Asia/Bangkok')
                st.dataframe(df,width=1500)
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
            total_env_list = influxdb_env_lists = ["INFLUX_SERVER","INFLUX_DATABASE","INFLUX_USER_LOGIN","INFLUX_PASSWORD","INFLUX_PORT","INFLUX_MEASUREMENT"]
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
                        client = InfluxDBClient(os.environ["INFLUX_SERVER"], os.environ["INFLUX_PORT"], os.environ["INFLUX_USER_LOGIN"], os.environ["INFLUX_PASSWORD"], os.environ["INFLUX_DATABASE"])
                        client.ping()
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
        return 1
    except Exception as e:
        # st.error(f"An error occurred: {e}")
        st.error(f"Spec_id is duplicated !!!")
        return 0
    finally:
        cursor.close()
        conn.close()

def config_master_spec():
    qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)
    col1,col2 = st.columns(2)
    with col1:
        with st.form("master_spec_form",clear_on_submit=False):
            st.markdown("""<h3 style='text-align: center;'>Master Spec Input</h3>""", unsafe_allow_html=True)
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
                spec_id = str(part_no)+"_"+str(process)+"_"+str(item_no)+"_"+str(rev)

                insert_spec_id = insert_to_db(spec_id,part_no,rev, process, item_no, item_check, spec_nominal, tolerance_max, tolerance_min, method, point, register)

    with col2:
        if (submit_button == 1) and  (insert_spec_id == 1):
            # Create and generate the QR code
            qr.add_data(spec_id)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            img_bytes = io.BytesIO()
            img.save(img_bytes)
            img_bytes.seek(0)
            st.image(img_bytes, caption=spec_id)
            st.markdown(f"**QR Code for Spec ID:** {spec_id}")
            
            st.download_button(label="Download QR Code",data=img_bytes,file_name=f"{spec_id}.png",mime="image/png")

def monitor_chart():
    st.write("Monitor data")
    with st.form("chart_form"):
        part_no,item_check,process,equipment_no = get_selectbox(os.environ["SERVER"],os.environ["USER_LOGIN"],os.environ["PASSWORD"],os.environ["DATABASE"],os.environ["TABLE_1"])

        col1,col2,col3,col4,col5,col6 = st.columns(6)
        with col1:
            if part_no:
                part_no_selectbox = st.selectbox("Select part_no",(part_no),index = None,key = 'part_no')
            else:
                st.markdown("No data")

        with col2:
            if item_check:
                itemcheck_selectbox = st.selectbox("Select item check",(item_check),index = None,key = 'item_check')
            else:
                st.markdown("No data")
        with col3:
            if process:
                process_selectbox = st.selectbox("Select process",(process),index = None, key = 'process')
            else:
                st.markdown("No data")
        with col4:
            if equipment_no:
                equipment_selectbox = st.selectbox("Select equipment",(equipment_no),index = None,key = 'equipment_no')
            else:
                st.markdown("No data")
        with col5:
            stdate_selectbox = st.date_input("Select start date" ,value = None)
        with col6:
            fndate_selectbox = st.date_input("Select finish date" ,value = None)
        submit = st.form_submit_button(label='Generate')
        if submit:
            chart_data(os.environ["SERVER"],os.environ["USER_LOGIN"],os.environ["PASSWORD"],os.environ["DATABASE"],os.environ["TABLE_1"],part_no_selectbox,itemcheck_selectbox,process_selectbox,equipment_selectbox,stdate_selectbox,fndate_selectbox)

def chart_data(server,user_login,password,database,table,part_no,item_check,process,equipment,stdate,fndate):
    try:
        cnxn = pymssql.connect(server, user_login, password, database)
        cursor = cnxn.cursor(as_dict=True)
        query = f"SELECT * FROM {table} WHERE time BETWEEN '{stdate}' AND '{fndate}' AND part_no = '{part_no}' AND item_check = '{item_check}' AND process = '{process}' AND equipment_no = '{equipment}'"
        cursor.execute(query)

        data = cursor.fetchall()
        cursor.close()
        cnxn.close()
        if data:
            df = pd.DataFrame(data)
            df['fnl_data'] = df['fnl_data'].astype(float)
            df['max'] = df['fnl_data'] + df['tolerance_max'].astype(float)
            df['min'] = df['fnl_data'] + df['tolerance_min'].astype(float)
            df = df[['time','fnl_data','max','min']]

            line_chart = alt.Chart(df).mark_line().encode(
                x='time:T', 
                y='fnl_data:Q',  
                tooltip=['time:T', 'fnl_data:Q', 'max:Q', 'min:Q']
            )
            point_chart = alt.Chart(df).mark_point().encode(
                x='time:T',
                y='fnl_data:Q',
                tooltip=['time:T', 'fnl_data:Q', 'max:Q', 'min:Q']
            )
            combined_chart = line_chart + point_chart
            st.altair_chart(combined_chart, use_container_width=True)

    except Exception as e:
        st.error(f'Error: {str(e)}', icon="❌")

def dataflow_production_influx():
        st.caption("INFLUXDB")
        cnxn = pymssql.connect(os.environ["SERVER"],os.environ["USER_LOGIN"],os.environ["PASSWORD"],os.environ["DATABASE"])
        cursor = cnxn.cursor(as_dict=True)
        cursor.execute(f'''SELECT TOP(5) * FROM {os.environ["MASTER_SPEC_TABLE"]}  order by register desc''')
        data = cursor.fetchall()
        cursor.close()
        cnxn.close()
        if data:
            df = pd.DataFrame(data)
            df = df.drop_duplicates(subset=['item_check'],keep='first')
            df = df[['spec_id']]

        preview_influx_selectbox = st.selectbox(
                "mqtt topic",
                df,
                index=None,
                placeholder="select topic...",
                key='preview_influx'
                    )
        if preview_influx_selectbox:
            preview_influx_but = st.button("QUERY",key="preview_influx_but")

            if preview_influx_but:
                spec_id  = preview_influx_selectbox
                preview_influx(st,os.environ["INFLUX_SERVER"],os.environ["INFLUX_PORT"],os.environ["INFLUX_USER_LOGIN"],os.environ["INFLUX_PASSWORD"],os.environ["INFLUX_DATABASE"],os.environ["QC_COLUMN_NAMES"],spec_id)
        st.markdown("---")

def dataflow_production_sql():
        st.caption("SQLSERVER")
        cnxn = pymssql.connect(os.environ["SERVER"],os.environ["USER_LOGIN"],os.environ["PASSWORD"],os.environ["DATABASE"])
        cursor = cnxn.cursor(as_dict=True)
        cursor.execute(f'''SELECT TOP(5) * FROM {os.environ["MASTER_SPEC_TABLE"]}  order by register desc''')
        data = cursor.fetchall()
        cursor.close()
        cnxn.close()
        if data:
            df = pd.DataFrame(data)
            df = df.drop_duplicates(subset=['item_check'],keep='first')
            df = df[['spec_id']]

        preview_sqlserver_selectbox = st.selectbox(
                "mqtt topic",
                df,
                index=None,
                placeholder="select topic...",
                key='preview_sqlserver'
                    )
        if preview_sqlserver_selectbox:
            preview_sqlserver_but = st.button("QUERY",key="preview_sqlserver_but")
        
            if preview_sqlserver_but:
                spec_id  = preview_sqlserver_selectbox
                preview_production_sqlserver(os.environ["SERVER"],os.environ["USER_LOGIN"],os.environ["PASSWORD"],os.environ["DATABASE"],os.environ["TABLE_1"],spec_id)
        st.markdown("---")

def main_layout():
    st.set_page_config(
            page_title="QC System",
            page_icon="💻",
            layout="wide",
            initial_sidebar_state="expanded",
        )
    st.markdown("""<h1 style='text-align: center;'>QC MONITORING SYSTEM</h1>""", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col2:
        text_input_container = st.empty()
        password = text_input_container.text_input("Input password", type="password")

    if password == "1":
        text_input_container.empty()
        tab1, tab2,tab3,tab4  = st.tabs(["📝 Dashboard", "⚙️ Project Configulation","🔑 DB Connection","🔍 Data Preview"])
        
        with tab1:
            pass
            # monitor_chart()

        with tab2:
            st.write("Master Configulation")
            config_master_spec()
        with tab3:
            st.write("DB Connection")
            config_db_connect("SQLSERVER")
            config_db_connect("INFLUXDB")
        with tab4:
            st.write("Master Spec Preview")
            preview_master_sqlserver(os.environ["SERVER"],os.environ["USER_LOGIN"],os.environ["PASSWORD"],os.environ["DATABASE"],os.environ["MASTER_SPEC_TABLE"])
            dataflow_production_influx()
            dataflow_production_sql()

    elif password == "":
        pass
    else:
        st.toast('PASSWORD NOT CORRECT!', icon='❌')

if __name__ == "__main__":
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    main_layout()