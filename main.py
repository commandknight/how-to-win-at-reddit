"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""


# TODO: Create getData file
import parent_post_pipeline

# import clean_parentPost_table_pipeline as clean_post
# import test

# This is the mainclass file, will control the pipeline
if __name__ == '__main__':
    #sql_manager.print_test()
    parent_post_pipeline.process_parent_data_pipeline()
    # clean_post.get_unique_parent_ids()
    #clean_post.clean_parentPost_table_pipeline()

    print("Hello world!")
