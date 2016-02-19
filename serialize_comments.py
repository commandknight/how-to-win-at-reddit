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
    return json.loads(string)