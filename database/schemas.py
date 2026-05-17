import sqlite3
import logging

logger = logging.getLogger(__name__)

def create_tables(cursor):
    tables = {
        "users":"""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin','staff')) DEFAULT 'staff',
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,

        "products": """
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,

        "customers": """
            CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL DEFAULT 'example@gmail.com',
                address TEXT NOT NULL DEFAULT 'chargulli',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """,

        "orders": """
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                total_amount REAL NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        """,

        "order_items": """
            CREATE TABLE IF NOT EXISTS order_items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL DEFAULT 0,
                FOREIGN KEY(order_id) REFERENCES orders(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """
    }

    for table in tables:
        try:
            cursor.execute(tables[table]) # type: ignore
            logger.info(f"[DB INFO ] {table} table created successfully.")
        except sqlite3.Error as e:
            logger.error(f"[DB ERROR ]  {table} table not created : {e}")
        
        