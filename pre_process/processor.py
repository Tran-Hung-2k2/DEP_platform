
import psycopg2
import os
import sys
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

"""
put config here
"""
from configs.config import config

db_name = config["TRACK_AND_TRACE_DB_NAME"]
db_user = config["TRACK_AND_TRACE_DB_USER"]
db_password = config["TRACK_AND_TRACE_DB_PASSWORD"]
db_host = config["TRACK_AND_TRACE_DB_HOST"]
db_port = config["TRACK_AND_TRACE_DB_PORT"]

class Preprocessing():
    def __init__(self, **kwargs):
        # Initialize database connection
        self.conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        self.current_db = None
        self.df = None

    def configurations(self):
        pass

    def connect_to_database(self, current_db_name="track_and_trace"):
            self.close_connection()
            if current_db_name == "track_and_trace":
                self.conn = psycopg2.connect(
                    database=config["TRACK_AND_TRACE_DB_NAME"],
                    user=config["TRACK_AND_TRACE_DB_USER"],
                    password=config["TRACK_AND_TRACE_DB_PASSWORD"],
                    host=config["TRACK_AND_TRACE_DB_HOST"],
                    port=config["TRACK_AND_TRACE_DB_PORT"],
                )
            else:
                print("Invalid database name.")
                return False

            try:
                self.cursor = self.conn.cursor()
                self.current_db = current_db_name
                print(f"Connected to the {current_db_name} database")
                return True
            except psycopg2.Error as e:
                print(f"Error connecting to the {current_db_name} database: {e}")
                return False


    def close_connection(self):
        if self.cursor:
            self.cursor.close()
            self.conn.close()
            print("Connection closed")

    def fetch_all(self):
        sql_query = f"SELECT * FROM {self.current_db}"
        self.df = pd.read_sql_query(sql_query, self.conn)
        if self.df.empty:
            print("No data found")
            return False             
        

    def get_data_by_user_id(self, user_id):
        sql_query = f"SELECT * FROM {self.current_db} WHERE user_id ={user_id}"
        df = pd.read_sql_query(sql_query, self.conn)
        if df.empty:
            print("No data matched")
            return False
        else:
            return df

    def get_data_by_device_id(self, device_id):
        sql_query = f"SELECT * FROM {self.current_db} WHERE user_id ={device_id}"
        df = pd.read_sql_query(sql_query, self.conn)
        if df.empty:
            print("No data matched")
            return False
        else:
            return df
        
    def get_data_by_filter(self, filter_data=None):
        if filter_data is None:
            print("Filter data must be provided.")
            return None
        try:
            df_filter = pd.DataFrame(filter_data.items(), columns=["field", "value"])
            conditions = []
            for _, row in df_filter.iterrows():
                field = row["field"]
                value = row["value"]
                if (
                    field == "Timestamp"
                    and isinstance(value, tuple)
                    and len(value) == 2
                ):
                    start, end = value
                    conditions.append(
                        f"{field.lower()} BETWEEN {start} AND {end}"
                    )
                else:
                    conditions.append(
                        f"{field.lower()} = '{value}'"
                    )
            sql_query = f'SELECT * FROM "Attributes" WHERE {" AND ".join(conditions)}'
            df = pd.read_sql_query(sql_query, self.conn)
            if df.empty:
                print("No data matched")
                return False
            else:
                return df

        except psycopg2.Error as e:
            print(f"Error getting attributes: {e}")
            self.conn.rollback()
            return None



if __name__ == '__main__':
    # all of test case locate here
    pass