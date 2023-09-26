# database server here
import psycopg2
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from user_manager import UserManager
from register_manager import RegisterManager
from device_manager import DeviceManager
from attributes_manager import AttributesManager
from pykafka import KafkaClient
from pykafka.simpleconsumer import OffsetType
import json
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from configs.config import config

db_name = config["USER_DB_NAME"]
db_user = config["USER_DB_USER"]
db_password = config["USER_DB_PASSWORD"]
db_host = config["USER_DB_HOST"]
db_port = config["USER_DB_PORT"]


def require_user_db_connection(func):
    def wrapper(self, *args, **kwargs):
        if self.current_db == "user_db":
            return func(self, *args, **kwargs)
        else:
            print("Not connected to user_db database.")
            return False

    return wrapper


def require_track_and_trace_connection(func):
    def wrapper(self, *args, **kwargs):
        if self.current_db == "track_and_trace":
            return func(self, *args, **kwargs)
        else:
            print("Not connected to track_and_trace database.")
            return False

    return wrapper


class DatabaseManager:
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
    @require_user_db_connection
    def create_user_table(self):
        return self.user_manager.create_user_table()

    @require_user_db_connection
    def add_user(self, user_data):
        return self.user_manager.add_user(user_data)

    @require_user_db_connection
    def get_user(self, user_id):
        return self.user_manager.get_user(user_id)

    @require_user_db_connection
    def get_user_by_username(self, user_name):
        return self.user_manager.get_user_by_username(user_name)

    @require_user_db_connection
    def update_user_by_username(self, user_name, new_data):
        return self.user_manager.update_user_by_username(user_name, new_data)

    @require_user_db_connection
    def delete_user(self, user_id):
        return self.user_manager.delete_user(user_id)

    # Gọi các phương thức từ DeviceManager
    @require_user_db_connection
    def create_device_table(self):
        return self.device_manager.create_device_table()

    @require_user_db_connection
    def add_device(self, device_data):
        return self.device_manager.add_device(device_data)

    @require_user_db_connection
    def get_device(self, device_id):
        return self.device_manager.get_device(device_id)

    @require_user_db_connection
    def get_device_by_user(self, user_id):
        return self.device_manager.get_device_by_user(user_id)

    @require_user_db_connection
    def update_device(self, device_id, new_data):
        return self.device_manager.update_device(device_id, new_data)

    @require_user_db_connection
    def delete_device(self, device_id):
        return self.device_manager.delete_device(device_id)

    # Gọi các phương thức từ RegisterManager
    @require_user_db_connection
    def create_register_table(self):
        return self.register_manager.create_register_table()

    @require_user_db_connection
    def add_register(self, register_data):
        return self.register_manager.add_register(register_data)

    @require_user_db_connection
    def get_register_by_user_id(self, user_id):
        return self.register_manager.get_register_by_user_id(user_id)

    @require_user_db_connection
    def update_register(self, token, new_data):
        return self.register_manager.update_register(token, new_data)

    @require_user_db_connection
    def delete_register(self, token):
        return self.register_manager.delete_register(token)

    # Gọi các phương thức từ AttributesManager
    @require_track_and_trace_connection
    def create_attributes_table(self):
        return self.attributes_manager.create_attributes_table()

    @require_track_and_trace_connection
    def add_attributes(self, attributes_data):
        return self.attributes_manager.add_attributes(attributes_data)

    @require_track_and_trace_connection
    def add_batch_attributes(self, batch_attributes_data=None):
        return self.attributes_manager.add_batch_attributes(batch_attributes_data)

    @require_track_and_trace_connection
    def get_attributes_by_id(self, attribute_id):
        return self.attributes_manager.get_attributes_by_id(attribute_id)

    def data_consume(self, host, port, topic):
        # Khởi tạo Kafka Client
        client = KafkaClient(hosts=f'{host}:{port}')
        # Xác định Consumer Group và topic
        consumer_group_name = "my_consumer_group"
        topic_name = topic

        # Tạo Kafka Consumer
        consumer = client.topics[topic_name].get_balanced_consumer(
            consumer_group=consumer_group_name,
            auto_commit_enable=True,
            auto_commit_interval_ms=1000,  # Thời gian tự động commit offset
            zookeeper_connect="localhost:22181"  # Địa chỉ ZooKeeper
        )

        # Bắt đầu lắng nghe các message từ topic
        for message in consumer:
            if message is not None:
                data = json.loads(message.value.decode('utf-8'))
                if self.data_preprocess(data):
                    self.add_attributes(data)
                else:
                    print("Falied Data")
                
        # Đóng kết nối sau khi hoàn thành
        consumer.stop()


    def data_preprocess(self, data):
        if data.get("Problem") == "TrackAndTrace" :
            device_id = data.get("DeviceID")
            print(device_id)
            return self.get_device(device_id) != None 

    def create_user_table_example(self):
        # Tạo bảng "user" nếu nó chưa tồn tại
        if self.create_user_table():
            print("User table created successfully.")
        else:
            print("Error creating user table.")

    def add_user_example(self):
        # Thêm người dùng mới
        new_user_data = {
            "UserID": "0123456789",
            "Username": "JohnDoe",
            "Password": "password123",
            "Gender": "Male",
            "Email": "john@example.com",
            "DateOfBirth": "1990-01-01",
            "PhoneNumber": "1234567890",
            "Balance": 1000.0,
            "UserRole": "User",
        }
        if self.add_user(new_user_data):
            print("User added successfully.")
        else:
            print("Error adding user.")

    def get_user_by_username_example(self):
        # Lấy thông tin người dùng bằng tên người dùng
        user = self.get_user_by_username("JohnDoe")
        if user:
            print(f"User found: {user}")
        else:
            print("User not found.")

    def update_user_example(self):
        # Cập nhật thông tin người dùng
        user_name_to_update = "JohnDoe"
        updated_user_data = {
            "Password": "newpassword123",
            "Gender": "Female",
            "Email": "newemail@example.com",
            "DateOfBirth": "1990-01-01",
            "PhoneNumber": "9876543210",
            "Balance": 1500.0,
            "UserRole": "Admin",
        }

        if self.update_user_by_username(user_name_to_update, updated_user_data):
            print("User updated successfully.")
        else:
            print("Error updating user.")

    def create_device_table_example(self):
        # Tạo bảng "device" nếu nó chưa tồn tại
        if self.create_device_table():
            print("Device table created successfully.")
        else:
            print("Error creating device table.")

    def add_device_example(self):
        # Thêm thiết bị mới
        new_device_data = {
            "DeviceID": "device123",
            "UserID": "0123456789",
            "DeviceName": "MyDevice",
            "PlateNo": "ABC123",
        }

        if self.add_device(new_device_data):
            print("Device added successfully.")
        else:
            print("Error adding device.")

    def get_device_example(self):
        # Lấy thông tin thiết bị bằng ID thiết bị
        device_id_to_get = "device123"
        device = self.get_device(device_id_to_get)
        if device:
            print(f"Device found: {device}")
        else:
            print("Device not found.")

    def update_device_example(self):
        device_id_to_update = "device123"
        updated_device_data = {
            "DeviceName": "UpdatedDeviceName",
        }

        if self.update_device(device_id_to_update, updated_device_data):
            print("Device updated successfully.")
        else:
            print("Error updating device.")

    def delete_device_example(self):
        # Xóa thiết bị bằng ID thiết bị
        device_id_to_delete = "device123"
        if self.delete_device(device_id_to_delete):
            print("Device deleted successfully.")
        else:
            print("Error deleting device.")

    def create_register_table_example(self):
        # Tạo bảng "register" nếu nó chưa tồn tại
        if self.create_register_table():
            print("Register table created successfully.")
        else:
            print("Error creating register table.")

    def add_register_example(self):
        new_register_data = {
            "Token": "token123",
            "UserID": "0123456789",
            "Problem": "Some problem description",
        }

        if self.add_register(new_register_data):
            print("Register added successfully.")
        else:
            print("Error adding register.")

    def get_register_example(self):
        token_to_get = "token123"
        register = self.get_register_by_user_id(token_to_get)  # Gọi từ RegisterManager
        if register:
            print(f"Register found: {register}")
        else:
            print("Register not found.")

    def delete_register_example(self):
        # Xóa đăng ký bằng token
        token_to_delete = "token123"
        if self.delete_register(token_to_delete):
            print("Register deleted successfully.")
        else:
            print("Error deleting register.")

    def delete_user_example(self):
        # Xóa người dùng bằng ID người dùng
        user_id_to_delete = "0123456789"
        if self.delete_user(user_id_to_delete):
            print("User deleted successfully.")
        else:
            print("Error deleting user.")


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect_to_database(current_db_name="user_db")

    # Gọi các ví dụ tương ứng cho các hàm
    # User
    db_manager.create_user_table_example()
    db_manager.add_user_example()
    db_manager.get_user_by_username_example()
    db_manager.update_user_example()

    # Device
    db_manager.create_device_table_example()
    db_manager.add_device_example()
    db_manager.get_device_example()
    db_manager.update_device_example()
    # db_manager.delete_device_example()

    # # Register
    # db_manager.create_register_table_example()
    # db_manager.add_register_example()
    # db_manager.get_register_example()
    # db_manager.delete_register_example()

    # # Delete user
    # # db_manager.delete_user_example()
    #kafka
    db_manager.data_consume("localhost",29092,"alo")
    # Kết thúc kết nối
    db_manager.close_connection()
