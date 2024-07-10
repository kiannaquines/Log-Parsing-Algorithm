import re
from concurrent.futures import ThreadPoolExecutor
from connection import multithreaded_connect_to_db
from utils import time_parser, get_file_in_log_folder
import os
from datetime import datetime

def process_line(line, pattern):
    match = pattern.match(line)
    if match:
        time, artist, advertisement = match.groups()
        return (time_parser(time), artist, advertisement)
    return None

def process_file(filename, pattern):
    connection, cursor = multithreaded_connect_to_db()
    processed = 0
    batch = []
    batch_size = 1000
    try:
        with open(os.path.join(os.getcwd(), 'logs', filename), 'r') as file:
            for line in file:
                result = process_line(line, pattern)
                if result:
                    batch.append(result)
                    if len(batch) >= batch_size:
                        cursor.executemany("INSERT INTO airtime_logs VALUES (?,?,?)", batch)
                        processed += len(batch)
                        batch = []
        if batch:
            cursor.executemany("INSERT INTO airtime_logs VALUES (?,?,?)", batch)
            processed += len(batch)
        connection.commit()
        print(f"Completed: {filename}, Processed: {processed} entries")
    except Exception as e:
        print(f"Error processing {filename}: {e}")
    finally:
        connection.close()

def main():
    files = get_file_in_log_folder()
    log_pattern = re.compile(r"(\d{2}-[A-Z][a-z]{2}-\d{4} \d{2}:\d{2}:\d{2}) (.*?) - (.*)")

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(process_file, file, log_pattern) for file in files]
        for future in futures:
            future.result()

    print("Processing of all files completed")

if __name__ == "__main__":
    start_time = datetime.now()
    main()
    time_lapse = datetime.now() - start_time
    print(f"Processing ended in {time_lapse.total_seconds():.2f} seconds")