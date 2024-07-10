import re
from connection import connect_to_db,threaded_connect_to_db
from utils import time_parser,read_log,get_file_in_log_folder
import os
from datetime import datetime
import threading


def process(filename, pattern):

    connection, cursor = threaded_connect_to_db()

    current_logs = read_log(os.path.join(os.getcwd(),'logs',filename))
    for log in current_logs:
        try:
            extracted_log = re.findall(pattern, string=log)
            extracted_log = [(time_parser(time), artist, advertisement) for time, artist, advertisement in extracted_log]
            if extracted_log:
                cursor.executemany("INSERT INTO airtime_logs VALUES (?,?,?)", extracted_log)
                connection.commit()
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")
            continue
            
    print("Completed: ", filename)

def main():
    files = get_file_in_log_folder()
    log_pattern = re.compile(r"(\d{2}-[A-Z][a-z]{2}-\d{4} \d{2}:\d{2}:\d{2}) (.*?) - (.*)")
    threads = []

    for file in files:
        thread = threading.Thread(target=process, args=(file, log_pattern))
        threads.append(thread)
        thread.start()
        thread.is_alive()
        
    for thread in threads:
        thread.join()

    print("Processing of file completed")
    
if __name__ == "__main__":
    start_time = datetime.now()
    main()
    time_lapse = datetime.now() - start_time
    print(f"Processing end at {time_lapse.total_seconds():.2f} seconds")
    
