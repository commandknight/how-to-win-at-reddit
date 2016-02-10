# Timothie's Comment Pipeline

"""
Create a pipeline method that for each parent post in parentPostDetail table, update comments field with list of ids (referring to May2015 table) of comments up to a certain time by calling get_children_commentsIDs for each parent ID
name: process_child_comments_pipeline()

Create a method that given a parent post ID, will get all the children posts up to a time limit X and return array of ids
name: get_children_commentsIDs()
"""

import sql_manager

def process_child_comments_pipeline():
    pass


def get_children_commentIDs(parentPost_id, time_limit):
    """
    Get children post IDs made within time_limit from when parentPost_id is made.
    :param parentPost_id: parent_id of comments to be found
    :param time_limit: time in minutes a comment must have been made after the parent was posted, to be included
    :return: array of children  IDs
    """
    pass

if __name__ == '__main__':
    print("Main to test comment pipeline")
    rdt = sql_manager
    test_data = rdt.get_test_data(rdt.timothie_path)
    for x in test_data:
        print(x)
    rdt.close_db_connection()