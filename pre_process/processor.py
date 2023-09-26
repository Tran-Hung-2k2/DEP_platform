
import psycopg2
import json
import os
import sys
from attributes_manager import AttributesManager

"""
put config here
"""
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from configs.config import config

class Preprocessing():
    def __init__(self, **kwargs):
        # initialize here
        pass

    def configurations(self):
        pass

    def connect_to_database(self, current_db_name="user_db"):
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
                if current_db_name == "track_and_trace":
                    self.user_manager = None
                    self.device_manager = None
                    self.register_manager = None
                    self.attributes_manager = AttributesManager(self.conn, self.cursor)

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

        ...

    def add_something(self, params):
        pass

    def update_something(self, params):
        pass

    def delete_something(self, params):
        pass

    def data_consume(self, params):
        pass

    def data_preprocess(self, params):
        pass
    ...

if __name__ == '__main__':
    # all of test case locate here
    pass