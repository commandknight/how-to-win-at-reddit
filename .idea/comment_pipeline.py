# Timothie's Comment Pipeline

"""
Create a pipeline method that for each parent post in parentPostDetail table, update comments field with list of ids (referring to May2015 table) of comments up to a certain time by calling get_children_commentsIDs for each parent ID
name: process_child_comments_pipeline()

Create a method that given a parent post ID, will get all the children posts up to a time limit X and return array of ids
name: get_children_commentsIDs()
"""

import sql_manager
import time

def process_child_comments_pipeline(parentPost_id, db_path=None, time_limit=60):
    """
    Pipeline to start a db connection, find comment_ids within time limit, and return any children comments
    :param parentPost_id: required - Parent post ID to be searched
    :param db_path: optional - db path for search, will default to Timothie's machine
    :param time_limit: optional - time limit to look for comments in minutes
    :return: list of children comment IDs within time limit
    """
    db_connection = get_db_connection(db_path)
    children_list = get_children_commentIDs(db_connection, parentPost_id, time_limit)
    db_connection.close_db_connection()
    return children_list


def get_children_commentIDs(db_connect, parentPost_id, time_limit):
    """
    Get children post IDs made within time_limit from when parentPost_id is made.
    :param db_connect: connection to db to be searched
    :param parentPost_id: parent_id of comments to be found
    :param time_limit: time in minutes a comment must have been made after the parent was posted, to be included
    :return: array of children  IDs
    """
    children_ids = []
    time_limit_epoch = time_limit * 60


    return children_ids


def get_db_connection(db_path):
    """
    Prepare the db for search, if not
    :param db_path: db path for search, will default to Timothie's machine if none provided
    :return: open connection to db
    """
    reddit_db = sql_manager

    if db_path is None:
        db_path = reddit_db.timothie_path

    reddit_db.open_db_connection(db_path)
    return reddit_db


if __name__ == '__main__':
    print("Main to test comment pipeline")
