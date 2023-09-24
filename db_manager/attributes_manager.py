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
            DeviceID VARCHAR(10),
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
            insert_query = sql.SQL(
                'INSERT INTO "Attributes" (DeviceID, Timestamp, Status, Speed, Direction, Longitude, Latitude, Extrainfo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            )
            self.cursor.execute(insert_query, attributes_data)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding attributes: {e}")
            self.conn.rollback()
            return False

    def add_bacth_attributes(self, batch_attributes_data=[]):
        try:
            """
            batch_attributes_data = [
                (
                    "device123",
                    "2023-09-24 10:30:00",
                    "running",
                    60.0,
                    90.0,
                    45.123456,
                    -78.987654,
                    {"info1": "value1", "info2": "value2"},
                ),
                ...
            ]
            """

            # Tạo truy vấn INSERT hàng loạt
            insert_query = sql.SQL(
                'INSERT INTO "Attributes" (DeviceID, Timestamp, Status, Speed, Direction, Longitude, Latitude, Extrainfo) VALUES {}'
            ).format(sql.SQL(",").join(sql.Placeholder() * len(batch_attributes_data)))
            self.cursor.execute(
                insert_query, [tuple(record) for record in batch_attributes_data]
            )
            self.conn.commit()
            print("Batch insert successful.")
        except psycopg2.Error as e:
            print(f"Error performing batch insert: {e}")
            self.conn.rollback()
            return False

    def get_attributes(self, attribute_id):
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

    def update_attributes(self, attribute_id, new_data):
        try:
            update_query = sql.SQL(
                'UPDATE "Attributes" SET DeviceID = %s, Timestamp = %s, Status = %s, Speed = %s, Direction = %s, Longitude = %s, Latitude = %s, Extrainfo = %s WHERE ID = %s'
            )
            self.cursor.execute(update_query, (*new_data, attribute_id))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating attributes: {e}")
            self.conn.rollback()
            return False

    def delete_attributes(self, attribute_id):
        try:
            delete_query = sql.SQL('DELETE FROM "Attributes" WHERE ID = %s')
            self.cursor.execute(delete_query, (attribute_id,))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting attributes: {e}")
            self.conn.rollback()
            return False
