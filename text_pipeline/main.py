"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""


# from text_pipeline import comment_db_manager


# import clean_parentPost_table_pipeline as clean_post

def get_data():
    """
    MAIN method to get data to train on
    possible TODO may be to select a number of datapoints to load
    :return: this will return an tuple(list_of_text, target_classification)
    """
    from text_pipeline import mysql_manager
    mysql_manager.get_parent_post_data(0)
    mysql_manager.close_connection()
    return ""

# This is the mainclass file, will control the pipeline
if __name__ == '__main__':
    get_data()
    # parent_post_pipeline.process_parent_data_pipeline()
    # clean_post.get_unique_parent_ids()
    #clean_post.clean_parentPost_table_pipeline()

    print("Hello world!")
