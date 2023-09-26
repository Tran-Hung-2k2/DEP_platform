from fastapi import Depends
from db_manager.db_manager import DatabaseManager

def get_db_manager():
    db_manager = DatabaseManager()
    db_manager.connect_to_database()    
    return db_manager
