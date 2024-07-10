import sqlite3
import os

def connect_to_db():
    connection = sqlite3.connect(os.path.join(os.getcwd(),'airtime_logs.db'))
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airtime_logs (
        date_aired DATETIME, 
        artist TEXT, 
        advertisement TEXT
    )""")

    return connection, cursor

def threaded_connect_to_db():
    connection = sqlite3.connect(os.path.join(os.getcwd(),'threaded_airtime_logs.db'),check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airtime_logs (
        date_aired DATETIME, 
        artist TEXT, 
        advertisement TEXT
    )""")

    return connection, cursor

def multithreaded_connect_to_db():
    connection = sqlite3.connect(os.path.join(os.getcwd(),'multithreaded_airtime_logs.db'),check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airtime_logs (
        date_aired DATETIME, 
        artist TEXT, 
        advertisement TEXT
    )""")

    return connection, cursor