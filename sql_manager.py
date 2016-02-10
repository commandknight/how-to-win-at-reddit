"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""

# Get the data

import sqlite3
jeet_path = '/Users/jnagda/Documents/Reddit_Comments/database.sqlite'
timothie_path = 'C:/Users/Timothie/Desktop/reddit-comments-may-2015/database.sqlite'
conn = None

def open_db_connetion(path):
    """
    Open the db connection to the local machine
    :param path: Path of local db
    """
    conn = sqlite3.connect(path)


def get_unique_parent_ids():
    """
    Function that returns list of unique link_IDs
    :return: list of strings (ids)
    """
    curr = conn.cursor()
    curr.execute('SELECT DISTINCT link_id FROM May2015')
    return curr.fetchall()


def get_test_data(path):
    """
    Returns first 10 rows of May2015 table as a sample test
    """
    conn = sqlite3.connect(path)
    result = conn.execute('SELECT * FROM May2015 LIMIT 10')
    return result


def create_parentPostDetail_table():
    """
    Function to create ParentPostDetail table in sqliteDB if it doesnt exist
    :return: result of cursor object execution
    """
    create_table_sql = "CREATE TABLE IF NOT EXISTS ParentPostDetails (parentPost_id TEXT PIMARY KEY NOT NULL," \
          "url TEXT," \
          "timecreated_utc INTEGER NOT NULL," \
          "subreddit_id TEXT NOT NULL," \
          "subreddit TEXT NOT NULL,title TEXT NOT NULL," \
          "score INTEGER,author TEXT NOT NULL," \
          "childrenComments BLOB);"
    result = conn.execute(create_table_sql)
    return result


def fill_parentPostDetail_with_test_data():
    """
    TEST Function to insert 2 dummy records into ParentPostDetail table
    :return: null
    """
    fd = open('sql_scripts/fakedata_parentPostDetail.sql','r')
    raw_text = fd.read()
    fd.close()
    records_to_insert = raw_text.split(';')
    c = conn.cursor()
    for record in records_to_insert:
        c.execute(record)
    conn.commit()


def print_test():
    """
    Function to print test data rows
    :return: null
    """
    for x in get_test_data():
        print(x)


def close_db_connection():
    """
    function to close DB connection
    """
    conn.close()
