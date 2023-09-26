import psycopg2
from psycopg2 import sql
import json

import pandas as pd

class AttributesManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_attributes_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "Attributes" (
            ID SERIAL PRIMARY KEY,
            DeviceID CHAR(10),
            Timestamp TIMESTAMP,
            Status VARCHAR(255),
            Speed FLOAT,
            Direction FLOAT,
            Longitude FLOAT,
            Latitude FLOAT,
            Extrainfo JSONB
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Attributes table created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating Attributes table: {e}")
            self.conn.rollback()

    def add_attributes(self, attributes_data):
        try:
            # Tạo tuple từ các giá trị
            data_tuple = (
                attributes_data.get("DeviceID"),
                attributes_data.get("Timestamp"),
                attributes_data.get("Status"),
                attributes_data.get("Speed"),
                attributes_data.get("Direction"),
                attributes_data.get("Longitude"),
                attributes_data.get("Latitude"),
                json.dumps(attributes_data.get("Extrainfo")),
            )

            insert_query = sql.SQL(
                'INSERT INTO "Attributes" (DeviceID, Timestamp, Status, Speed, Direction, Longitude, Latitude, Extrainfo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            )
            self.cursor.execute(insert_query, data_tuple)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding attributes: {e}")
            self.conn.rollback()
            return False

    def add_batch_attributes(self, batch_attributes_data=None):
        if batch_attributes_data is None:
            batch_attributes_data = []
        try:
            # Tạo truy vấn INSERT hàng loạt
            insert_query = sql.SQL(
                'INSERT INTO "Attributes" (DeviceID, Timestamp, Status, Speed, Direction, Longitude, Latitude, Extrainfo) VALUES {}'
            ).format(sql.SQL(",").join(sql.Placeholder() * len(batch_attributes_data)))

            # Biến đổi danh sách các dict thành danh sách các tuple
            records = [
                (
                    record.get("DeviceID"),
                    record.get("Timestamp"),
                    record.get("Status"),
                    record.get("Speed"),
                    record.get("Direction"),
                    record.get("Longitude"),
                    record.get("Latitude"),
                    json.dumps(record.get("Extrainfo")),
                )
                for record in batch_attributes_data
            ]

            self.cursor.execute(insert_query, records)
            self.conn.commit()
            print("Batch insert successful.")
            return True
        except psycopg2.Error as e:
            print(f"Error performing batch insert: {e}")
            self.conn.rollback()
            return False

    def get_attributes_by_id(self, attribute_id):
        try:
            select_query = sql.SQL('SELECT * FROM "Attributes" WHERE ID = %s')
            self.cursor.execute(select_query, (attribute_id,))
            attributes_row = self.cursor.fetchone()

            if attributes_row:
                columns = [desc[0] for desc in self.cursor.description]
                attributes_dict = dict(zip(columns, attributes_row))
                return attributes_dict
            else:
                print("Attributes not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error getting attributes: {e}")
            self.conn.rollback()
            return None

    def get_attributes(self, filter_data=None):
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
                        )
                    )
                    values.extend([start, end])
                else:
                    conditions.append(
                        sql.SQL("{} = %s").format(sql.Identifier(field.lower()))
                    )
                    values.append(value)

            select_query = sql.SQL('SELECT * FROM "Attributes" WHERE {}').format(
                sql.SQL(" AND ").join(conditions)
            )

            self.cursor.execute(select_query, values)
            attributes_rows = self.cursor.fetchall()

            attributes_list = []
            columns = [desc[0] for desc in self.cursor.description]

            for attributes_row in attributes_rows:
                attributes_dict = dict(zip(columns, attributes_row))
                attributes_list.append(attributes_dict)

            if attributes_list:
                return attributes_list
            else:
                print("Attributes not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error getting attributes: {e}")
            self.conn.rollback()
            return None
