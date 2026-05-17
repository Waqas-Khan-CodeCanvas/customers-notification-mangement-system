import sqlite3
import logging
from configs.constants import DATABASE_NAME

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.conn.row_factory = sqlite3.Row  # must be immediately after connect
            self.conn.execute("PRAGMA foreign_keys = ON;")

            logger.info("Database connected successfully.")
            return self.conn
        except sqlite3.Error as e:
            logger.error(f"Database connection failed : {e}")

    def get_cursor(self):
        if not self.conn:
            self.connect()
        return self.conn.cursor() # type: ignore

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()
    
    def close(self):
        if self.conn:
            self.conn.close()

db  = Database()

def initialize_database():
    from database.schemas import create_tables
    db.connect()
    create_tables(db.get_cursor())
    