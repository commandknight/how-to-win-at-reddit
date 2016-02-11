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
import time

import praw

import sql_manager


def truncate_identifier_from_id(id):
    return id[3:]


def get_parentpost_json(parentPost):
    user_agent = "PyAI UCI-CS175 0.2"
    link_id = truncate_identifier_from_id(parentPost[0])
    url_string = 'https://www.reddit.com/r/' + parentPost[1] + '/comments/' + link_id + '/.json'
    # print(url_string) #DEBUG PRINT STATEMENT
    r = praw.Reddit(user_agent=user_agent)
    t = r.get_submission(url_string)
    return vars(t)


# TODO: FINISH THIS METHOD
def insert_parent_json_into_parentPostDetail(json_info):
    # extract json info
    # sql_manager.insert_parent_detail(list_of_info)
    pass


def process_parentPostID(parent_id):
    insert_parent_json_into_parentPostDetail(get_parentpost_json(parent_id))


def process_parent_data_pipeline():
    start_time = time.time()
    for parent_id in sql_manager.get_unique_parent_ids():
        print(parent_id)
        process_parentPostID(parent_id)
    print("--- %s seconds ---" % (time.time() - start_time))
