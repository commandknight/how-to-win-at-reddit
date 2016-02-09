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
import sql_manager

def get_parentpost_json(parentPost_id):
    #use praw (reddit API to fetch JSON of reddit page)
    pass


def insert_parent_json_into_parentPostDetail(json_info):
    # extract json info
    # sql_manager.insert_parent_detail(list_of_info)
    pass


def process_parentPostID(parent_id):
    insert_parent_json_into_parentPostDetail(get_parentpost_json(parent_id))


def process_parent_data_pipeline():
    for parent_id in sql_manager.get_unique_parent_ids():
        get_parentpost_json(parent_id)
    pass