# This module uses JSON to serialize and deserialize a python list
# Will be used to interpret and upload information to MySQL as BLOB

import json


def serialize_list(list):
    '''
    serializes list into a string
    :param list:
    :return string:
    '''
    return json.dumps(list)


def deserialize_list(string):
    '''
    deserialize string into a list
    :param string:
    :return list:
    '''
    return json.loads(string.decode('latin-1'))
