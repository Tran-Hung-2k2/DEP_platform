import psycopg2
from psycopg2 import sql


class RegisterManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_register_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "register" (
            Token VARCHAR(255) PRIMARY KEY,
            UserID VARCHAR(10) REFERENCES "user" (UserID)
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
            insert_query = sql.SQL(
                'INSERT INTO "register" (Token, UserID) VALUES (%s, %s)'
            )
            self.cursor.execute(insert_query, register_data)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding register: {e}")
            self.conn.rollback()
            return False

    def get_register(self, token):
        try:
            select_query = sql.SQL('SELECT * FROM "register" WHERE Token = %s')
            self.cursor.execute(select_query, (token,))
            register = self.cursor.fetchone()
            if register:
                return register
            else:
                print("Register not found.")
                return None
        except psycopg2.Error as e:
            print(f"Error getting register: {e}")
            self.conn.rollback()
            return None

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
