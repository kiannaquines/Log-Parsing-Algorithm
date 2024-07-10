import re
from connection import connect_to_db
from utils import time_parser,read_log,get_file_in_log_folder
import os
from datetime import datetime

def main(cursor, connection):
    files = get_file_in_log_folder()
    log_pattern = re.compile(r"(\d{2}-[A-Z][a-z]{2}-\d{4} \d{2}:\d{2}:\d{2}) (.*?) - (.*)")
    
    for file in files:
        current_logs = read_log(os.path.join(os.getcwd(),'logs',file))
        for log in current_logs:
            try:
                extracted_log = re.findall(log_pattern, string=log)
                extracted_log = [(time_parser(time), artist, advertisement) for time, artist, advertisement in extracted_log]
                if extracted_log:
                    cursor.executemany("INSERT INTO airtime_logs VALUES (?,?,?)", extracted_log)
                    connection.commit()
            except Exception as e:
                continue
        print("Completed: ", file)

    print("Completed ", len(files), " files.")

if __name__ == "__main__":
    connection, cursor = connect_to_db()
    try:
        start_time = datetime.now()
        main(cursor=cursor, connection=connection)
        time_lapse = datetime.now() - start_time
        print(f"Processing end at {time_lapse.total_seconds():.2f} seconds")
    finally:
        connection.close()