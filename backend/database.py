import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "data", "ecommerce.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    # This allows us to access columns by name (dict-like)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_products():
    """
    Fetches the master inventory array from the database.
    """
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    
    # Convert Row objects to standard dictionaries for our service layer
    return [dict(p) for p in products]
