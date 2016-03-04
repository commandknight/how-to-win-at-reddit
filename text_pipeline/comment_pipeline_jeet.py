# Jeet's Comment Pipeline

"""
Create a pipeline method that for each parent post in parentPostDetail table, update comments field with list of ids (referring to May2015 table) of comments up to a certain time by calling get_children_commentsIDs for each parent ID
name: process_child_comments_pipeline()

Create a method that given a parent post ID, will get all the children posts up to a time limit X and return array of ids
name: get_children_commentsIDs()

"""
import time

from text_pipeline import comment_db_manager
from text_pipeline import mysql_manager

def process_child_comments_pipeline(parentPost_id, time_limit=180):
    """
    Pipeline to start a db connection, find comment_ids within time limit, and return any children comments
    :param parentPost_id: required - Parent post ID to be searched
    :param comment_db_path: optional - db path for search, will default to Timothie's machine
    :param time_limit: optional - time limit to look for comments in minutes
    :return: list of children comment IDs within time limit ?????
    """
    children_list = get_children_commentIDs(parentPost_id, time_limit)
    mysql_manager.update_parentPost(children_list, parentPost_id)
    # comment_db_manager.close_db_connection()
    # return children_list


def get_children_commentIDs(parentPost_id, time_limit):
    """
    Get children post IDs made within time_limit from when parentPost_id is made.
    :param comment_path: path to local comment db to be connected to
    :param parent_connect: connection to the parent_id db
    :param parentPost_id: parent_id of comments to be found
    :param time_limit: time in minutes a comment must have been made after the parent was posted, to be included
    :return: array of children  IDs
    """
    children_ids = []
    time_limit_epoch = time_limit * 60

    parent_post_info = mysql_manager.get_parent_created_info(parentPost_id)
    children = comment_db_manager.get_children_comments(parentPost_id)
    parent_post_time = int(float(parent_post_info[1]))
    ## DEBUG PRINT STATEMENTS
    # print("INFO",parent_post_info)
    # print("CHILDREN",children)
    # print("UTC",parent_post_time)
    ## END DEBUG PRINT STATEMENTS

    cutoff_time_limit = parent_post_time + time_limit_epoch
    p_time = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(parent_post_time))
    c_time = 0;
    children_ids = [x for x, y, z, a in children]
    # print(children_ids)
    # print(len(children_ids))
    # for id,parent_id,link_id,created_time in children:
    #     if created_time < cutoff_time_limit:
    #         children_ids.append(id)
    #         c_time = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(created_time))
    # print("Total children: " + str(len(children)) + " | After time cutoff: " + str(len(children_ids)))
    # print("Parent post time: " + str(p_time) + " | Last child within time limit: " + str(c_time))
    return children_ids


def update_all_mysql_parent_posts():
    print("GETTING IDS")
    list_of_ids = mysql_manager.get_parent_post_ids()
    print("GOT IDS:" + str(len(list_of_ids)))
    x = 0
    for (parent_id,) in list_of_ids:
        print("PROCESSING: " + parent_id + " ---iter -- " + str(x))
        x += 1
        process_child_comments_pipeline(parent_id)


if __name__ == '__main__':
    update_all_mysql_parent_posts()
    mysql_manager.close_connection()
    comment_db_manager.close_db_connection()
    # parent_id = 't3_37y5rx', 'AskReddit'
    # parent_dict = []
    # parent = parent_post_pipeline.get_parentpost_dict(parent_id)
    # print(parent)
    # parent_dict.append(parent)
    # mysql_manager.insert_parentdetails_BIG(parent_dict)
    # process_child_comments_pipeline('t3_37y5rx')
    # process_child_comments_pipeline('t3_37zlq2')
    # process_child_comments_pipeline('t3_37w2go')
    # process_child_comments_pipeline('t3_37zyk6')
    # process_child_comments_pipeline('t3_37yawp')
