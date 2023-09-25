# database server here
import psycopg2
import json
import os
import sys
from user_manager import UserManager
from register_manager import RegisterManager
from device_manager import DeviceManager
from attributes_manager import AttributesManager

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from configs.config import config

db_name = config["USER_DB_NAME"]
db_user = config["USER_DB_USER"]
db_password = config["USER_DB_PASSWORD"]
db_host = config["USER_DB_HOST"]
db_port = config["USER_DB_PORT"]


class DatabaseManage:
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
        # Tạo các instance cho các manager
        self.user_manager = None
        self.device_manager = None
        self.register_manager = None
        self.attributes_manager = None

    def configurations(self):
        # You can implement any database configurations here if needed
        pass

    def connect_to_database(self, current_db_name="user_db"):
        self.close_connection()
        if current_db_name == "user_db":
            self.conn = psycopg2.connect(
                database=config["USER_DB_NAME"],
                user=config["USER_DB_USER"],
                password=config["USER_DB_PASSWORD"],
                host=config["USER_DB_HOST"],
                port=config["USER_DB_PORT"],
            )
        elif current_db_name == "track_and_trace":
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

            if current_db_name == "user_db":
                self.user_manager = UserManager(self.conn, self.cursor)
                self.device_manager = DeviceManager(self.conn, self.cursor)
                self.register_manager = RegisterManager(self.conn, self.cursor)
                self.attributes_manager = None
            elif current_db_name == "track_and_trace":
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

    # Gọi các phương thức từ UserManager
    def create_user_table(self):
        if self.current_db == "user_db":
            return self.user_manager.create_user_table()
        else:
            print("Not connected to user_db database.")
            return False

    def add_user(self, user_data):
        if self.current_db == "user_db":
            return self.user_manager.add_user(user_data)
        else:
            print("Not connected to user_db database.")
            return False

    def get_user(self, user_id):
        if self.current_db == "user_db":
            return self.user_manager.get_user(user_id)
        else:
            print("Not connected to user_db database.")
            return False

    def update_user(self, user_id, new_data):
        if self.current_db == "user_db":
            return self.user_manager.update_user(user_id, new_data)
        else:
            print("Not connected to user_db database.")
            return False

    def delete_user(self, user_id):
        if self.current_db == "user_db":
            return self.user_manager.delete_user(user_id)
        else:
            print("Not connected to user_db database.")
            return False

    # Gọi các phương thức từ DeviceManager
    def create_device_table(self):
        if self.current_db == "user_db":
            return self.device_manager.create_device_table()
        else:
            print("Not connected to user_db database.")
            return False

    def add_device(self, device_data):
        if self.current_db == "user_db":
            return self.device_manager.add_device(device_data)
        else:
            print("Not connected to user_db database.")
            return False

    def get_device(self, device_id):
        if self.current_db == "user_db":
            return self.device_manager.get_device(device_id)
        else:
            print("Not connected to user_db database.")
            return False

    def update_device(self, device_id, new_data):
        if self.current_db == "user_db":
            return self.device_manager.update_device(device_id, new_data)
        else:
            print("Not connected to user_db database.")
            return False

    def delete_device(self, device_id):
        if self.current_db == "user_db":
            return self.device_manager.delete_device(device_id)
        else:
            print("Not connected to user_db database.")
            return False

    # Gọi các phương thức từ RegisterManager
    def create_register_table(self):
        if self.current_db == "user_db":
            return self.register_manager.create_register_table()
        else:
            print("Not connected to user_db database.")
            return False

    def add_register(self, register_data):
        if self.current_db == "user_db":
            return self.register_manager.add_register(register_data)
        else:
            print("Not connected to user_db database.")
            return False

    def get_register(self, token):
        if self.current_db == "user_db":
            return self.register_manager.get_register(token)
        else:
            print("Not connected to user_db database.")
            return False

    def delete_register(self, token):
        if self.current_db == "user_db":
            return self.register_manager.delete_register(token)
        else:
            print("Not connected to user_db database.")
            return False

    # Gọi các phương thức từ AttributesManager
    def create_attributes_table(self):
        if self.current_db == "track_and_trace":
            return self.attributes_manager.create_attributes_table()
        else:
            print("Not connected to track_and_trace database.")
            return False

    def add_attributes(self, attributes_data):
        if self.current_db == "track_and_trace":
            return self.attributes_manager.add_attributes(attributes_data)
        else:
            print("Not connected to track_and_trace database.")
            return False

    def get_attributes(self, attribute_id):
        if self.current_db == "track_and_trace":
            return self.attributes_manager.get_attributes(attribute_id)
        else:
            print("Not connected to track_and_trace database.")
            return False

    def update_attributes(self, attribute_id, new_data):
        if self.current_db == "track_and_trace":
            return self.attributes_manager.update_attributes(attribute_id, new_data)
        else:
            print("Not connected to track_and_trace database.")
            return False

    def delete_attributes(self, attribute_id):
        if self.current_db == "track_and_trace":
            return self.attributes_manager.delete_attributes(attribute_id)
        else:
            print("Not connected to track_and_trace database.")
            return False

    def data_consume(self, params):
        pass

    def data_preprocess(self, params):
        pass


if __name__ == "__main__":
    db_manager = DatabaseManage()
    db_manager.connect_to_database()

    # Tạo bảng User
    db_manager.create_user_table()

    # Ví dụ quản lý User
    new_user_data = {
        "UserID": "user123",
        "Username": "JohnDoe",
        "Password": "password123",
        "Gender": "Male",
        "Email": "john@example.com",
        "DateOfBirth": "1990-01-01",
        "PhoneNumber": "1234567890",
        "Balance": 1000.0,
        "UserRole": "User",
    }

    if db_manager.add_user(new_user_data):
        print("User added successfully.")

    user_id_to_get = "user123"
    user = db_manager.get_user(user_id_to_get)
    if user:
        print(f"User found: {user}")

    user_id_to_update = "user123"
    updated_user_data = {
        "Username": "JohnDoeUpdated",
        "Password": "newpassword123",
        "Gender": "Female",
        "Email": "newemail@example.com",
        "DateOfBirth": "1990-01-01",
        "PhoneNumber": "9876543210",
        "Balance": 1500.0,
        "UserRole": "Admin",
    }

    if db_manager.update_user(user_id_to_update, updated_user_data):
        print("User updated successfully.")

    # # Tạo bảng Device
    # db_manager.create_device_table()

    # # Ví dụ quản lý Device
    # new_device_data = (
    #     "device123",
    #     "user123",
    #     "MyDevice",
    #     "ABC123",
    # )

    # if db_manager.add_device(new_device_data):
    #     print("Device added successfully.")

    # device_id_to_get = "device123"
    # device = db_manager.get_device(device_id_to_get)
    # if device:
    #     print(f"Device found: {device}")

    # device_id_to_update = "device123"
    # updated_device_data = (
    #     "UpdatedDeviceName",
    #     "XYZ789",
    # )

    # if db_manager.update_device(device_id_to_update, updated_device_data):
    #     print("Device updated successfully.")

    # device_id_to_delete = "device123"
    # if db_manager.delete_device(device_id_to_delete):
    #     print("Device deleted successfully.")

    # # Tạo bảng Register
    # db_manager.create_register_table()

    # # Ví dụ quản lý Register
    # new_register_data = (
    #     "token123",
    #     "user123",
    # )

    # if db_manager.add_register(new_register_data):
    #     print("Register added successfully.")

    # token_to_get = "token123"
    # register = db_manager.get_register(token_to_get)
    # if register:
    #     print(f"Register found: {register}")

    # token_to_delete = "token123"
    # if db_manager.delete_register(token_to_delete):
    #     print("Register deleted successfully.")

    # user_id_to_delete = "user123"
    # if db_manager.delete_user(user_id_to_delete):
    #     print("User deleted successfully.")

    # db_manager.connect_to_database(current_db_name="track_and_trace")

    # # Tạo bảng Attributes
    # db_manager.create_attributes_table()

    # # Example: Add Attributes
    # new_attributes_data = (
    #     "device123",
    #     "2023-09-24 10:30:00",
    #     "running",
    #     60.0,
    #     90.0,
    #     45.123456,
    #     -78.987654,
    #     json.dumps({"info1": "value1", "info2": "value2"}),
    # )
    # if db_manager.add_attributes(new_attributes_data):
    #     print("Attributes added successfully.")

    # # Example: Get Attributes by ID
    # attribute_id_to_get = 1  # Replace with the desired attribute ID
    # attributes = db_manager.get_attributes(attribute_id_to_get)
    # if attributes:
    #     print(f"Attributes found: {attributes}")

    # # Example: Update Attributes
    # attribute_id_to_update = 1  # Replace with the desired attribute ID
    # updated_attributes_data = (
    #     "device123",
    #     "2023-09-24 11:45:00",
    #     "stopped",
    #     0.0,
    #     180.0,
    #     46.987654,
    #     -77.123456,
    #     json.dumps({"info3": "value3", "info4": "value4"}),
    # )
    # if db_manager.update_attributes(attribute_id_to_update, updated_attributes_data):
    #     print("Attributes updated successfully.")

    # # Example: Delete Attributes
    # attribute_id_to_delete = 1
    # if db_manager.delete_attributes(attribute_id_to_delete):
    #     print("Attributes deleted successfully.")

    db_manager.close_connection()
