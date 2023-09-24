import psycopg2
from psycopg2 import sql


class UserManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def create_user_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "user" (
            UserID VARCHAR(10) PRIMARY KEY,
            Username VARCHAR(255),
            Password VARCHAR(255),
            Gender VARCHAR(255),
            Email VARCHAR(255),
            DateOfBirth DATE,
            PhoneNumber VARCHAR(255),
            Balance DECIMAL(10, 2),
            UserRole VARCHAR(255)
        )
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
            insert_query = sql.SQL(
                'INSERT INTO "user" (UserID, Username, Password, Gender, Email, DateOfBirth, PhoneNumber, Balance, UserRole) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            )
            self.cursor.execute(insert_query, user_data)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error adding user: {e}")
            self.conn.rollback()
            return False

    def get_user(self, user_id):
        try:
            select_query = sql.SQL('SELECT * FROM "user" WHERE UserID = %s')
            self.cursor.execute(select_query, (user_id,))
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

    def update_user(self, user_id, new_data):
        try:
            update_query = sql.SQL(
                'UPDATE "user" SET Username = %s, Password = %s, Gender = %s, Email = %s, DateOfBirth = %s, PhoneNumber = %s, Balance = %s, UserRole = %s WHERE UserID = %s'
            )
            self.cursor.execute(update_query, (*new_data, user_id))
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
