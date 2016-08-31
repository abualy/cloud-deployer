# Encoding: '' UTF-8

import os.path
import json

def merge(first, second, path=None):
    if path is None:
        path = []
    for key in second:
        if key in first:
            if isinstance(first[key], dict) and isinstance(second[key], dict):
                merge(first[key], second[key], path + [str(key)])
            elif first[key] == second[key]:
                pass
            else:
                first[key] = second[key]
        else:
            first[key] = second[key]
    return first


def load_config_file(file_to_load, dictionary=None):
    """
    Load a configuration file in json format
    """
    if dictionary is None:
        dictionary = {}
    with open(file_to_load) as data_file:
        data = json.load(data_file)
        if "imports" in data:
            for file_to_import in data['imports']:
                child_data = load_config_file(os.path.dirname(file_to_load)+'/'+file_to_import)
                dictionary = merge(dictionary, child_data)
            del data['imports']

    dictionary = merge(dictionary, data)
    return dictionary
