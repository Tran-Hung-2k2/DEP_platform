import psycopg2
from psycopg2 import sql


class RegisterManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_register_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "register" (
            Token CHAR(15) PRIMARY KEY,
            UserID CHAR(10) REFERENCES "user" (UserID),
            Problem VARCHAR(50)
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Register table created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating register table: {e}")
            self.conn.rollback()

    def add_register(self, register_data):
        try:
            # Tạo tuple từ các giá trị trích xuất
            data_tuple = (
                register_data.get("Token"),
                register_data.get("UserID"),
                register_data.get("Problem"),
            )

            insert_query = sql.SQL(
                'INSERT INTO "register" (Token, UserID, Problem) VALUES (%s, %s, %s)'
            )
            self.cursor.execute(insert_query, data_tuple)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding register: {e}")
            self.conn.rollback()
            return False

    def get_register_by_user_id(self, user_id):
        try:
            select_query = sql.SQL('SELECT * FROM "register" WHERE UserID = %s')
            self.cursor.execute(select_query, (user_id,))
            register = self.cursor.fetchone()
            if register:
                return register
            else:
                print("Register not found for the specified UserID.")
                return None
        except psycopg2.Error as e:
            print(f"Error getting register by UserID: {e}")
            self.conn.rollback()
            return None

    def update_register(self, token, new_data):
        try:
            # Tạo danh sách các phần của câu truy vấn SQL
            set_statements = []
            update_values = []

            # Xử lý từng cặp key-value trong new_data
            for key, value in new_data.items():
                if key not in ["Token"]:
                    set_statements.append(f"{key} = %s")
                    update_values.append(value)

            # Thêm giá trị Token vào danh sách update_values
            update_values.append(token)

            # Xây dựng câu truy vấn SQL
            update_query = (
                f'UPDATE "register" SET {", ".join(set_statements)} WHERE Token = %s'
            )

            # Thực hiện câu truy vấn cập nhật
            self.cursor.execute(update_query, tuple(update_values))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error updating register: {e}")
            self.conn.rollback()
            return False

    def delete_register(self, token):
        try:
            delete_query = sql.SQL('DELETE FROM "register" WHERE Token = %s')
            self.cursor.execute(delete_query, (token,))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error deleting register: {e}")
            self.conn.rollback()
            return False
