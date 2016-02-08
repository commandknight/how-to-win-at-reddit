# JEET's Parent Post Module Pipeline
"""
Create method that creates a new post detail table in sqlite if it doesn’t exist already
name: create_parentPostDetail_table()
Create method that fetches JSON of the parent post for a given key of a parent post and returns JSON of the
 parent post only [NOTE: will need to use Reddit API to fetch JSON, this is not in the May2015 table]
name: get_parentpost_json()
Create method that gets unique ids for parent posts from May2015 comment data using sql statement in
 sqlmanager and then fetches json for each parent, returns dictionary
name: get_all_parentpost_ids()
Create a pipeline processing method: 1 - calls get_all_parentpost_ids,
 2- for each id calls get_parentpost_json, 3- inserts each json data into a new sqlite table
name: process_parent_data_pipeline()
"""


def create_parentPostDetail_table():
    # create dbConn
    # create sql prepared statement to create table
        # create table if not exists TableName (col1 typ1, ..., colN typN)
    # execute sql_prepared statement
    # close dbConn
    pass


def fill_parentPostDetail_with_test_data():
    # insert fake row 1
    # insert fake row 2
    pass

def get_parentpost_json():
    pass

def get_all_parentpost_ids():
    pass

def process_parent_data_pipeline():
    pass