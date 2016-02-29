"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""


# from text_pipeline import comment_db_manager

from text_pipeline import parent_post_pipeline
from text_pipeline import serialize_comments as sc

# import clean_parentPost_table_pipeline as clean_post




def get_training_data():
    from text_pipeline import mysql_manager
    all_records = mysql_manager.get_parent_post_data()
    mysql_manager.close_connection()
    from text_pipeline import comment_db_manager as cdm
    training_data = []
    target_data = [1 if record[2] > 414 else 0 for record in all_records]
    for parentPost_id, childrenComments, score, url, selftext in all_records:
        # get_text_of_post
        post_text = url + selftext
        # get_text_of_children
        children_text = ""
        for comment_id in sc.deserialize_list(childrenComments):
            children_text += cdm.get_children_text_features(comment_id)
        training_data.append(post_text + children_text)
    cdm.close_db_connection()
    return training_data, target_data


# This is the mainclass file, will control the pipeline
if __name__ == '__main__':
    # get_data()
    parent_post_pipeline.process_parent_data_pipeline()
    # clean_post.get_unique_parent_ids()
    #clean_post.clean_parentPost_table_pipeline()

    print("Hello world!")
