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

from text_pipeline import comment_db_manager


def truncate_identifier_from_id(id):
    return id[3:]


def get_parentpost_dict(parentPost):
    user_agent = "PyAI UCI-CS175 0.2"
    link_id = truncate_identifier_from_id(parentPost[0])
    url_string = 'https://www.reddit.com/r/' + parentPost[1] + '/comments/' + link_id + '/.json'
    # print(url_string) #DEBUG PRINT STATEMENT
    r = praw.Reddit(user_agent=user_agent)
    try:
        t = r.get_submission(url_string)
        parent_info = vars(t)
        parentDict = {
            'author': '[deleted]' if parent_info['author'] is None else parent_info['author'].name,
            'id': parentPost[0],
            'url': parent_info['url'],
            'timecreated': parent_info['created_utc'],
            'subreddit_id': parent_info['subreddit_id'],
            'subreddit': parent_info['subreddit'].display_name,
            'title': parent_info['title'],
            'score': parent_info['score'],
            'selftext': '[deleted]' if parent_info['selftext'] is None else parent_info['selftext']
        }
        return parentDict
    except:
        return


"""
def process_parentPostID(parent_id):
    mysql_manager.insert_parent_dict_into_parentPostDetail(parent_id, get_parentpost_dict(parent_id))
"""

def process_parent_data_pipeline():
    start_time = time.time()
    x = 0
    list_of_dicts = []
    for parent_id in comment_db_manager.get_unique_parent_ids():
        print("GETTING:", x, parent_id)
        temp = get_parentpost_dict(parent_id)
        if temp is not None:
            list_of_dicts.append(temp)
        x += 1
    from text_pipeline import mysql_manager
    mysql_manager.insert_parentdetails_BIG(list_of_dicts)
    print("--- %s seconds ---" % (time.time() - start_time))
    comment_db_manager.close_db_connection()
    mysql_manager.close_connection()
