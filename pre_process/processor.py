
import psycopg2
from psycopg2 import sql
import json
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
        self.cursor = None
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

    def get_data_by_user_id(self, user_id):
        sql_query = f"SELECT * FROM {self.current_db} WHERE user_id ={user_id}"
        self.df = pd.read_sql_query(sql_query, self.conn)

    def get_data_by_device_id(self, device_id):
        sql_query = f"SELECT * FROM {self.current_db} WHERE user_id ={device_id}"
        self.df = pd.read_sql_query(sql_query, self.conn)
        
    def get_data_by_filter(self, filter_data=None):
        if filter_data is None:
            print("Filter data must be provided.")
            return None
        try:
            conditions = []
            values = []
            for field, value in filter_data.items():
                # Kiểm tra nếu trường là "Timestamp" và giá trị là một tuple (start, end)
                if (
                    field == "Timestamp"
                    and isinstance(value, tuple)
                    and len(value) == 2
                ):
                    start, end = value
                    conditions.append(
                        sql.SQL("{} BETWEEN %s AND %s").format(
                            sql.Identifier(field.lower())
                        )  # Chuyển tên cột thành chữ thường ở đây
                    )
                    values.extend([start, end])
                else:
                    conditions.append(
                        sql.SQL("{} = %s").format(sql.Identifier(field.lower()))
                    )  # Chuyển tên cột thành chữ thường ở đây
                    values.append(value)

            select_query = sql.SQL('SELECT * FROM "Attributes" WHERE {}').format(
                sql.SQL(" AND ").join(conditions)
            )

            self.cursor.execute(select_query, values)
            attributes = self.cursor.fetchall()

            if attributes:
                return attributes
            else:
                print("Attributes not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error getting attributes: {e}")
            self.conn.rollback()
            return None


    def delete_something(self, params):
        pass

    def data_preprocess(self, params):
        pass
    ...

if __name__ == '__main__':
    # all of test case locate here
    pass