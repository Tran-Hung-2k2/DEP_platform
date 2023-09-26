import psycopg2
from psycopg2 import sql
import json

# import pandas as pd


class AttributesManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_attributes_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "attributes" (
            id SERIAL PRIMARY KEY,
            device_id CHAR(10),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(255),
            speed FLOAT,
            direction FLOAT,
            longitude FLOAT,
            latitude FLOAT,
            extra_info JSONB
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
                attributes_data.get("device_id"),
                attributes_data.get("timestamp"),
                attributes_data.get("status"),
                attributes_data.get("speed"),
                attributes_data.get("direction"),
                attributes_data.get("longitude"),
                attributes_data.get("latitude"),
                json.dumps(attributes_data.get("extra_info")),
            )

            insert_query = sql.SQL(
                'INSERT INTO "attributes" (device_id, timestamp, status, speed, direction, longitude, latitude, extra_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
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
                'INSERT INTO "attributes" (device_id, timestamp, status, speed, direction, longitude, latitude, extra_info) VALUES {}'
            ).format(sql.SQL(",").join(sql.Placeholder() * len(batch_attributes_data)))

            # Biến đổi danh sách các dict thành danh sách các tuple
            records = [
                (
                    record.get("device_id"),
                    record.get("timestamp"),
                    record.get("status"),
                    record.get("speed"),
                    record.get("direction"),
                    record.get("longitude"),
                    record.get("latitude"),
                    json.dumps(record.get("extra_info")),
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
            select_query = sql.SQL('SELECT * FROM "attributes" WHERE id = %s')
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
                    field == "timestamp"
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

            select_query = sql.SQL('SELECT * FROM "attributes" WHERE {}').format(
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
