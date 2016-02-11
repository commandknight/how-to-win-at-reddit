"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""


# TODO: Create getData file
import parent_post_pipeline

# This is the mainclass file, will control the pipeline
if __name__ == '__main__':
    #sql_manager.print_test()
    parent_post_pipeline.process_parent_data_pipeline()
    print("Hello world!")
