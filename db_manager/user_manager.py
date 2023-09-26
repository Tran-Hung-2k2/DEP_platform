import psycopg2
from psycopg2 import sql


class UserManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_user_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "user" (
            user_id CHAR(10) PRIMARY KEY,
            user_name VARCHAR(40) UNIQUE,
            password VARCHAR(255),
            gender VARCHAR(10),
            email VARCHAR(100),
            date_of_birth DATE,
            phone_number VARCHAR(15),
            balance FLOAT,
            role VARCHAR(50)
        );
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("User table created successfully.")
            return True
        except psycopg2.Error as e:
            print(f"Error creating user table: {e}")
            self.conn.rollback()
            return False

    def add_user(self, user_data):
        try:
            # Chuyển đổi từ dictionary thành tuple
            data_tuple = (
                user_data.get("user_id"),
                user_data.get("user_name"),
                user_data.get("password"),
                user_data.get("gender"),
                user_data.get("email"),
                user_data.get("date_of_birth"),
                user_data.get("phone_number"),
                user_data.get("balance"),
                user_data.get("role"),
            )

            insert_query = sql.SQL(
                'INSERT INTO "user" (user_id, user_name, password, gender, email, date_of_birth, phone_number, balance, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            )
            self.cursor.execute(insert_query, data_tuple)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding user: {e}")
            self.conn.rollback()
            return False

    def get_user(self, user_id):
        try:
            select_query = sql.SQL('SELECT * FROM "user" WHERE user_id = %s')
            self.cursor.execute(select_query, (user_id,))
            user = self.cursor.fetchone()
            if user:
                columns = [desc[0] for desc in self.cursor.description]
                user_dict = dict(zip(columns, user))
                return user_dict
            else:
                print("User not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error getting user: {e}")
            self.conn.rollback()
            return None

    def get_user_by_username(self, user_name):
        try:
            select_query = sql.SQL('SELECT * FROM "user" WHERE user_name = %s')
            self.cursor.execute(select_query, (user_name,))
            user = self.cursor.fetchone()

            if user:
                columns = [desc[0] for desc in self.cursor.description]
                user_dict = dict(zip(columns, user))
                return user_dict
            else:
                print("User with user_name =", user_name, "not found")
                return None
        except psycopg2.Error as e:
            print(f"Error getting user: {e}")
            self.conn.rollback()
            return None

    def update_user_by_username(self, user_name, new_data):
        try:
            # Tạo danh sách các phần của câu truy vấn SQL
            set_statements = []
            update_values = []

            # Xử lý từng cặp key-value trong new_data
            for key, value in new_data.items():
                if key not in ["user_name", "user_id"]:
                    set_statements.append(f"{key} = %s")
                    update_values.append(value)

            # Thêm giá trị UserID vào danh sách update_values
            update_values.append(user_name)

            # Xây dựng câu truy vấn SQL
            update_query = (
                f'UPDATE "user" SET {", ".join(set_statements)} WHERE user_name = %s'
            )

            # Thực hiện câu truy vấn cập nhật
            self.cursor.execute(update_query, tuple(update_values))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating user: {e}")
            self.conn.rollback()
            return False

    def delete_user(self, user_id):
        try:
            delete_query = sql.SQL('DELETE FROM "user" WHERE user_id = %s')
            self.cursor.execute(delete_query, (user_id,))
            deleted_count = self.cursor.rowcount  # Số lượng bản ghi đã bị xóa

            if deleted_count > 0:
                self.conn.commit()  # Commit nếu có bản ghi bị xóa
                return True
            else:
                return False
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")
            self.conn.rollback()
            return False
