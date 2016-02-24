# Timothie's Comment Pipeline

"""
Create a pipeline method that for each parent post in parentPostDetail table, update comments field with list of ids (referring to May2015 table) of comments up to a certain time by calling get_children_commentsIDs for each parent ID
name: process_child_comments_pipeline()

Create a method that given a parent post ID, will get all the children posts up to a time limit X and return array of ids
name: get_children_commentsIDs()
"""

import mysql_manager
import sql_manager

from text_pipeline import serialize_comments


def process_child_comments_pipeline(parentPost_id, comment_db_path=None, time_limit=180):
    """
    Pipeline to start a db connection, find comment_ids within time limit, and return any children comments
    :param parentPost_id: required - Parent post ID to be searched
    :param comment_db_path: optional - db path for search, will default to Timothie's machine
    :param time_limit: optional - time limit to look for comments in minutes
    :return: nothing
    """
    # parent_db_connection = mysql_manager
    parent_db_connection = None
    children_list = get_children_commentIDs(comment_db_path, parent_db_connection, parentPost_id, time_limit)
    print(children_list)
    parent_update(parent_db_connection, parentPost_id, children_list)
    #parent_db_connection.close_connection()


def get_children_commentIDs(comment_path, parent_connect, parentPost_id, time_limit):
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
    parent_post_info = mysql_manager.perform_query(parent_query_string)
    children = query_comment_db(comment_path, children_query_string)
    for(parentPost_id, timecreated_utc) in parent_post_info:
        parent_post_time = int(float(timecreated_utc))
    cutoff_time_limit = parent_post_time + time_limit_epoch
    for x,y,z,a in children:
        children_ids.append(x)
        # if a >= parent_post_time and a <= cutoff_time_limit:
        #     children_ids.append(x)
        #     print(x, y, z)
    return children_ids


def parent_update(parent_connect, parentPost_id, children_ids):
    """
    Update given parentPost with its serialized list of children_ids
    :param parent_connect: connection to mysql with parent post information
    :param parentPost_id: id of parent post to update
    :param children_ids: list of children ids
    :return: none
    """
    sl = serialize_comments
    serialized_children = sl.serialize_list(children_ids)
    mysql_manager.update_parentPost(serialized_children, parentPost_id)


def query_comment_db(db_path, query):
    """
    Prepare the db for search, if not
    :param db_path: db path for search, will default to Timothie's machine if none provided
    :param query: string for query to be performed on comment_db
    :return: list of comment db query result
    """
    query_results = []
    reddit_db = sql_manager

    if db_path is None:
        db_path = reddit_db.timothie_path

    query_results = reddit_db.perform_query(db_path, query)
    return query_results


if __name__ == '__main__':
    q = ('SELECT parentPost_id, title FROM ParentPostDetails LIMIT 2000')
    # my = mysql_manager
    q_results = mysql_manager.perform_query(q)
    #my.close_connection()

    for x,y in q_results:
        print(x + " | " + y)
        process_child_comments_pipeline(x)
    #process_child_comments_pipeline('t3_34gitq')
    #process_child_comments_pipeline('t3_10v5wy')
    #process_child_comments_pipeline('t3_10v5wy')
    #res = mysql_manager.perform_query('SELECT timecreated_utc FROM ParentPostDetails WHERE parentPost_id = \'t3_36i6nn\'')
    #print(res)
    #res = mysql_manager.perform_query('SELECT parentPost_id, COUNT(*) FROM ParentPostDetails GROUP BY parentPost_id HAVING COUNT(*) > 1')
    #for x in res:
    #    print(x)
    #process_child_comments_pipeline('t3_36i6nn')
