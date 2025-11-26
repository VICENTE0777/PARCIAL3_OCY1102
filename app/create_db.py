# app/create_db.py
import sqlite3
from werkzeug.security import generate_password_hash

DB = "database.db"

def create_schema():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()

def seed():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    users = [
        ("admin", generate_password_hash("Admin123!"), "admin"),
        ("user", generate_password_hash("User123!"), "user")
    ]
    for u,p,r in users:
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (u,p,r))
        except Exception:
            pass
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_schema()
    seed()
    print("Base de datos creada.")
