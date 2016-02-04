"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""

# Get the data

import sqlite3

def get_test_data():
    """

    :return:
    """
    conn = sqlite3.connect('/Users/jnagda/Documents/Reddit_Comments/database.sqlite')
    return conn.execute('SELECT * FROM May2015 LIMIT 10')


def print_test():
    for x in get_test_data():
        print(x)
