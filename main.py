import re
from connection import connect_to_db
from utils import time_parser,read_log
import os


def main(cursor, connection):
    current_logs = read_log(os.path.join(os.getcwd(), 'logs/2024-07-08-playlog.txt'))

    for log in current_logs:
        extracted_log = re.findall(pattern=r"(\d{2}-[A-Z][a-z]{2}-\d{4} \d{2}:\d{2}:\d{2}) (.*?) - (.*)", string=log)
        extracted_log = [(time_parser(time), artist, advertisement) for time, artist, advertisement in extracted_log]

        if extracted_log:
            cursor.executemany("INSERT INTO airtime_logs VALUES (?,?,?)", extracted_log)
            connection.commit()

if __name__ == "__main__":
    connection, cursor = connect_to_db()
    
    try:
        main(cursor=cursor, connection=connection)
    finally:
        connection.close()
