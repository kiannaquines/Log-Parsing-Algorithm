import sqlite3
import os

def connect_to_db():
    connection = sqlite3.connect(os.path.join(os.getcwd(), 'log_parsing.db'))
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airtime_logs (
        date_aired DATETIME, 
        artist TEXT, 
        advertisement TEXT
    )""")

    return connection, cursor