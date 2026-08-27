import sqlite3
import json
import os
import sys

# Ensure we can import from backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.database import DB_FILE, get_db_connection

JSON_FILE = os.path.join(BASE_DIR, "data", "products.json")

def init_db():
    print(f"Initializing database at {DB_FILE}...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            rating INTEGER NOT NULL,
            image TEXT
        )
    """)
    
    # Clear existing data
    cursor.execute("DELETE FROM products")
    
    # Load JSON and insert
    try:
        with open(JSON_FILE, "r") as f:
            products = json.load(f)
            
        for p in products:
            cursor.execute("""
                INSERT INTO products (id, name, category, price, rating, image)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (p['id'], p['name'], p['category'], p['price'], p['rating'], p['image']))
            
        conn.commit()
        print(f"Successfully inserted {len(products)} products into the database.")
    except Exception as e:
        print(f"Failed to load products: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
