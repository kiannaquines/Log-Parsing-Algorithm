from datetime import datetime
from os import walk, getcwd

def time_parser(time_str):
    return datetime.strptime(time_str, '%d-%b-%Y %H:%M:%S')

def read_log(path):
    with open(path, 'r') as file:
        list_logs = file.read().split('\n')
    return list_logs


def get_file_in_log_folder():
    list_of_files = []
    for (dirpath, dirnames, filenames) in walk(getcwd() + '/logs'):
        list_of_files.append(filenames)
    
    return list_of_files[0]