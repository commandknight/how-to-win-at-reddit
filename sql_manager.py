"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""

# Get the data

import sqlite3


def get_test_data():
    """
    Returns first 10 rows of May2015 table as a sample test
    """
    conn = sqlite3.connect('/Users/jnagda/Documents/Reddit_Comments/database.sqlite')
    result = conn.execute('SELECT * FROM May2015 LIMIT 10')
    conn.close()
    return result


def print_test():
    for x in get_test_data():
        print(x)
