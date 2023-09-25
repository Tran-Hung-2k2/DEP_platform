import psycopg2
from psycopg2 import sql


class DeviceManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_device_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "device" (
            DeviceID CHAR(10) PRIMARY KEY,
            UserID CHAR(10) REFERENCES "user" (UserID),
            DeviceName VARCHAR(255),
            PlateNo VARCHAR(20) UNIQUE
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Device table created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating device table: {e}")
            self.conn.rollback()

    def add_device(self, device_data):
        try:
            data_tuple = (
                device_data.get("DeviceID"),
                device_data.get("UserID"),
                device_data.get("DeviceName"),
                device_data.get("PlateNo"),
            )

            insert_query = sql.SQL(
                'INSERT INTO "device" (DeviceID, UserID, DeviceName, PlateNo) VALUES (%s, %s, %s, %s)'
            )
            self.cursor.execute(insert_query, data_tuple)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding device: {e}")
            self.conn.rollback()
            return False

    def get_device(self, device_id):
        try:
            select_query = sql.SQL('SELECT * FROM "device" WHERE DeviceID = %s')
            self.cursor.execute(select_query, (device_id,))
            device = self.cursor.fetchone()
            if device:
                return device
            else:
                print("Device not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error getting device: {e}")
            self.conn.rollback()
            return None

    def get_device_by_user(self, user_id):
        try:
            select_query = sql.SQL('SELECT * FROM "device" WHERE UserID = %s')
            self.cursor.execute(select_query, (user_id,))
            devices = self.cursor.fetchall()
            return devices
        except psycopg2.Error as e:
            print(f"Error getting devices for user: {e}")
            self.conn.rollback()
            return []

    def update_device(self, device_id, new_data):
        try:
            update_query = sql.SQL(
                'UPDATE "device" SET DeviceName = %s, PlateNo = %s WHERE DeviceID = %s'
            )
            self.cursor.execute(update_query, (*new_data, device_id))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating device: {e}")
            self.conn.rollback()
            return False

    def delete_device(self, device_id):
        try:
            delete_query = sql.SQL('DELETE FROM "device" WHERE DeviceID = %s')
            self.cursor.execute(delete_query, (device_id,))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting device: {e}")
            self.conn.rollback()
            return False
