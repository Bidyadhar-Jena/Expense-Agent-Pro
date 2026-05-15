import sqlite3

conn = sqlite3.connect("expense.db", check_same_thread=False)
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password BLOB
)
""")

# TRANSACTIONS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    name TEXT,
    amount REAL,
    category TEXT
)
""")

conn.commit()


def add_user(username, password):
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()


def get_user(username):
    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )
    return cursor.fetchone()


def add_transaction(username, name, amount, category):
    cursor.execute(
        "INSERT INTO transactions (username, name, amount, category) VALUES (?, ?, ?, ?)",
        (username, name, amount, category)
    )
    conn.commit()


def get_transactions(username):
    cursor.execute(
        "SELECT name, amount, category FROM transactions WHERE username=?",
        (username,)
    )
    return cursor.fetchall()