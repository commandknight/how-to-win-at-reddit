"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""


# TODO: Create getData file
import sql_manager

# This is the mainclass file, will control the pipeline
if __name__ == '__main__':
    #sql_manager.print_test()
    test = sql_manager.get_unique_parent_ids()
    print("Hello world!")
