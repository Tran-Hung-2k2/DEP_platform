import psycopg2
from psycopg2 import sql


class UserManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_user_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "user" (
            UserID CHAR(10) PRIMARY KEY,
            Username VARCHAR(40) UNIQUE,
            Password VARCHAR(50),
            Gender VARCHAR(10),
            Email VARCHAR(100),
            DateOfBirth DATE,
            PhoneNumber VARCHAR(15),
            Balance DECIMAL(10, 2),
            UserRole VARCHAR(50)
        );
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("User table created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating user table: {e}")
            self.conn.rollback()

    def add_user(self, user_data):
        try:
            # Chuyển đổi từ dictionary thành tuple
            data_tuple = (
                user_data.get("UserID"),
                user_data.get("Username"),
                user_data.get("Password"),
                user_data.get("Gender"),
                user_data.get("Email"),
                user_data.get("DateOfBirth"),
                user_data.get("PhoneNumber"),
                user_data.get("Balance"),
                user_data.get("UserRole"),
            )

            insert_query = sql.SQL(
                'INSERT INTO "user" (UserID, Username, Password, Gender, Email, DateOfBirth, PhoneNumber, Balance, UserRole) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            )
            self.cursor.execute(insert_query, data_tuple)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding user: {e}")
            self.conn.rollback()
            return False

    def get_user(self, user_name):
        try:
            select_query = sql.SQL('SELECT * FROM "user" WHERE Username = %s')
            self.cursor.execute(select_query, (user_name,))
            user = self.cursor.fetchone()
            if user:
                return user
            else:
                print("User not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error getting user: {e}")
            self.conn.rollback()
            return None

    def update_user(self, user_name, new_data):
        try:
            # Tạo danh sách các phần của câu truy vấn SQL
            set_statements = []
            update_values = []

            # Xử lý từng cặp key-value trong new_data
            for key, value in new_data.items():
                if key not in ["Username", "UserID"]:
                    set_statements.append(f"{key} = %s")
                    update_values.append(value)

            # Thêm giá trị UserID vào danh sách update_values
            update_values.append(user_name)

            # Xây dựng câu truy vấn SQL
            update_query = (
                f'UPDATE "user" SET {", ".join(set_statements)} WHERE Username = %s'
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
            delete_query = sql.SQL('DELETE FROM "user" WHERE UserID = %s')
            self.cursor.execute(delete_query, (user_id,))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")
            self.conn.rollback()
            return False
