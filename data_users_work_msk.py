import sqlite3
from sqlite3 import Error

# Connect to the SQLite database
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect(':memory:') # create a database in RAM
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

# Create a table
def create_table(conn):
    try:
        sql = """CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY,
                    first_name text NOT NULL,
                    last_name text,
                    is_premium integer,
                    is_subscribed integer
                );"""
        conn.execute(sql)
    except Error as e:
        print(e)

# Insert a new user
def insert_user(conn, user):
    sql = ''' INSERT INTO users(id,first_name,last_name,is_premium,is_subscribed)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

# Check if a user exists
def check_user(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    rows = cur.fetchall()
    return rows

# Update a user's subscription status
def update_subscription(conn, user):
    sql = ''' UPDATE users
              SET is_subscribed = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()

# Your bot code here...