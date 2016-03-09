# Jeet's Comment Pipeline

"""
Create a pipeline method that for each parent post in parentPostDetail table, update comments field with list of ids (referring to May2015 table) of comments up to a certain time by calling get_children_commentsIDs for each parent ID
name: process_child_comments_pipeline()

Create a method that given a parent post ID, will get all the children posts up to a time limit X and return array of ids
name: get_children_commentsIDs()

"""

from text_pipeline import comment_db_manager
from text_pipeline import mysql_manager


def process_child_comments_pipeline(parentPost_id):
    """
    Pipeline to start a db connection, find comment_ids within time limit, and return any children comments
    :param parentPost_id: required - Parent post ID to be searched
    """
    children_list = get_children_commentIDs(parentPost_id)
    mysql_manager.update_parentPost(children_list, parentPost_id)


def get_children_commentIDs(parentPost_id):
    """
    Get children post IDs made within time_limit from when parentPost_id is made.
    :param parentPost_id: parent_id of comments to be found
    :return: array of children  IDs
    """
    children = comment_db_manager.get_children_comments(parentPost_id)
    children_ids = [x for x, y, z, a in children]
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
    # process_child_comments_pipeline('t3_37y5rx')
    # process_child_comments_pipeline('t3_37zlq2')
    # process_child_comments_pipeline('t3_37w2go')
    # process_child_comments_pipeline('t3_37zyk6')
    # process_child_comments_pipeline('t3_37yawp')
