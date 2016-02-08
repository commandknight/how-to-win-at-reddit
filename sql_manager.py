"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""

# Get the data

import sqlite3

jeet_path = '/Users/jnagda/Documents/Reddit_Comments/database.sqlite'
conn = sqlite3.connect(jeet_path)

def get_test_data():
    """
    Returns first 10 rows of May2015 table as a sample test
    """
    conn = sqlite3.connect(jeet_path)
    result = conn.execute('SELECT * FROM May2015 LIMIT 10')
    return result


def create_parentPostDetail_table():
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
    fd = open('fakedata_parentPostDetail.sql','r')
    raw_text = fd.read()
    fd.close()
    records_to_insert = raw_text.split(';')
    c = conn.cursor()
    for record in records_to_insert:
        c.execute(record)
    conn.commit()


def print_test():
    for x in get_test_data():
        print(x)

def close_db_connection():
    conn = sqlite3.connect(jeet_path)
    conn.close()