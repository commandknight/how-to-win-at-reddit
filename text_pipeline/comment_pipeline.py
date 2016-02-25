# Timothie's Comment Pipeline

"""
Create a pipeline method that for each parent post in parentPostDetail table, update comments field with list of ids (referring to May2015 table) of comments up to a certain time by calling get_children_commentsIDs for each parent ID
name: process_child_comments_pipeline()

Create a method that given a parent post ID, will get all the children posts up to a time limit X and return array of ids
name: get_children_commentsIDs()

"""
import time

from text_pipeline import comment_db_manager
from text_pipeline import mysql_manager
from text_pipeline import parent_post_pipeline


def process_child_comments_pipeline(parentPost_id, comment_db_path=None, time_limit=180):
    """
    Pipeline to start a db connection, find comment_ids within time limit, and return any children comments
    :param parentPost_id: required - Parent post ID to be searched
    :param comment_db_path: optional - db path for search, will default to Timothie's machine
    :param time_limit: optional - time limit to look for comments in minutes
    :return: list of children comment IDs within time limit
    """
    parent_db_connection = mysql_manager
    curr = parent_db_connection.create_cursor()
    children_list = get_children_commentIDs(curr, comment_db_path, parent_db_connection, parentPost_id, time_limit)
    mysql_manager.update_parentPost(curr, children_list, parentPost_id)
    parent_db_connection.close_connection(curr)

    return children_list


def get_children_commentIDs(curr, comment_path, parent_connect, parentPost_id, time_limit):
    """
    Get children post IDs made within time_limit from when parentPost_id is made.
    :param comment_path: path to local comment db to be connected to
    :param parent_connect: connection to the parent_id db
    :param parentPost_id: parent_id of comments to be found
    :param time_limit: time in minutes a comment must have been made after the parent was posted, to be included
    :return: array of children  IDs
    """
    children_ids = []
    parent_post_time = 0
    time_limit_epoch = time_limit * 60

    parent_query = ('SELECT parentPost_id, timecreated_utc FROM ParentPostDetails WHERE parentPost_id = \'', parentPost_id, '\'')
    children_query = ('SELECT id, parent_id, link_id, created_utc FROM May2015 WHERE link_id = \'', parentPost_id, '\'')
    parent_query_string = ''.join(parent_query)
    children_query_string = ''.join(children_query)

    parent_post_info = parent_connect.perform_query(curr, parent_query_string)
    children = query_comment_db(comment_path, children_query_string)

    for(parentPost_id, timecreated_utc) in parent_post_info:
        parent_post_time = int(float(timecreated_utc))

    cutoff_time_limit = parent_post_time + time_limit_epoch
    p_time = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(parent_post_time))
    c_time = 0;

    for x,y,z,a in children:
        if a < cutoff_time_limit:
            children_ids.append(x)
            c_time = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(a))

    print("Total children: " + str(len(children)) + " | After time cutoff: " + str(len(children_ids)))
    print("Parent post time: " + str(p_time) + " | Last child within time limit: " + str(c_time))
    return children_ids


def query_comment_db(db_path, query):
    """
    Prepare the db for search, if not
    :param db_path: db path for search, will default to Timothie's machine if none provided
    :param query: string for query to be performed on comment_db
    :return: list of comment db query result
    """
    query_results = []
    reddit_db = comment_db_manager

    if db_path is None:
        db_path = reddit_db.timothie_desktop

    conn = reddit_db.open_db_connection(db_path)
    query_results = reddit_db.perform_query(conn, query)
    reddit_db.close_db_connection(conn)
    return query_results


if __name__ == '__main__':
    parent_id = 't3_37y5rx', 'AskReddit'
    parent_dict = []
    parent = parent_post_pipeline.get_parentpost_dict(parent_id)
    print(parent)
    parent_dict.append(parent)
    mysql_manager.insert_parentdetails_BIG(parent_dict)
    process_child_comments_pipeline('t3_37y5rx')

    # process_child_comments_pipeline('t3_37zlq2')
    # process_child_comments_pipeline('t3_37w2go')
    # process_child_comments_pipeline('t3_37zyk6')
    # process_child_comments_pipeline('t3_37yawp')
