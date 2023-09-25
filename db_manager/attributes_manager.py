import psycopg2
from psycopg2 import sql


class AttributesManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_attributes_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "Attributes" (
            ID SERIAL PRIMARY KEY,
            DeviceID CHAR(10), kiem tra da co deviceID
            Timestamp TIMESTAMP,not null (tu ren)
            Status VARCHAR(255), not null
            Speed FLOAT, not null
            Direction FLOAT,
            Longitude FLOAT, not null
            Latitude FLOAT, not null
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
                attributes_data.get("Extrainfo"),
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
            """
            batch_attributes_data = [
                {
                    "DeviceID": "device123",
                    "Timestamp": "2023-09-24 10:30:00",
                    "Status": "running",
                    "Speed": 60.0,
                    "Direction": 90.0,
                    "Longitude": 45.123456,
                    "Latitude": -78.987654,
                    "Extrainfo": {"info1": "value1", "info2": "value2"},
                },
                ...
            ]
            """

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
                    record.get("Extrainfo"),
                )
                for record in batch_attributes_data
            ]

            self.cursor.execute(insert_query, records)
            self.conn.commit()
            print("Batch insert successful.")
        except psycopg2.Error as e:
            print(f"Error performing batch insert: {e}")
            self.conn.rollback()
            return False

    def get_attributes_by_id(self, attribute_id):
        try:
            select_query = sql.SQL('SELECT * FROM "Attributes" WHERE ID = %s')
            self.cursor.execute(select_query, (attribute_id,))
            attributes = self.cursor.fetchone()
            if attributes:
                return attributes
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
                        sql.SQL("{} BETWEEN %s AND %s").format(sql.Identifier(field))
                    )
                    values.extend([start, end])
                else:
                    conditions.append(sql.SQL("{} = %s").format(sql.Identifier(field)))
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
