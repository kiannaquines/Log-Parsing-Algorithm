from datetime import datetime

def time_parser(time_str):
    return datetime.strptime(time_str, '%d-%b-%Y %H:%M:%S')

def read_log(path):
    with open(path, 'r') as file:
        list_logs = file.read().split('\n')
    return list_logs


