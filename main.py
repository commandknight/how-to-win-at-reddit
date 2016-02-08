"""
CS 175 - How To Win At Reddit
Jeet Nagda, Timothie Fujita, Jocelyne Perez
"""


# TODO: Create getData file
import sql_manager

# This is the mainclass file, will control the pipeline
if __name__ == '__main__':
    #sql_manager.print_test()
    sql_manager.create_parentPostDetail_table()
    sql_manager.fill_parentPostDetail_with_test_data()
    print("Hello world!")
