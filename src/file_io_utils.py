""" 
@file_name: file_io_utils.py
@author: Netmind.AI BlackSheep team 
@date: 2024-1-10 
Read and write the json file. 
"""


import json


def read_json(file_path):
    """
    Read JSON file and return a list of data
    """
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]
    return data

def save_list_dict_json(data, file_path):
    """
    save a list of data to a JSON file
    """
    with open(file_path, 'w') as file:
        for line in data:
            json.dump(line, file)
            file.write('\n')   
            
def save_json(data, file_path):
    """
    save a dict of data to a JSON file
    """
    with open(file_path, 'w') as file:
        json.dump(data, file)
            
