import numpy as np
import matplotlib.pyplot as  plt
import mysql_manager
import sql_manager
#import clean_parentPost_table_pipeline
import text_clean_test



### create a histogram of the languages in the database
### create a histogram of the size of each mainPost
### create a histogram of the size of the number of children (comments and subcomments)
###     that one mainPost has

conn = mysql_manager.cnx
conn_lite = sql_manager.open_db_connection(sql_manager.joc_path)

def data_stats():

    #MySQL data
    c =  conn.cursor()
    c.execute("SELECT COUNT(*) FROM ParentPostDetails")
    size = c.fetchone()
    print("MySQL DB size: " + str(size[0]))


    #sqlite3 data
    c_lite = conn_lite.cursor()
    c_lite.execute("SELECT COUNT(*) FROM May2015")
    size = c_lite.fetchone()
    print("sqlite3 DB size: " + str(size[0]))



def histogram_of_languages():
    c =  conn.cursor()
    c.execute("SELECT selftext FROM ParentPostDetails")
    language_array = []

    for x in range(1000):
        text = c.fetchone()
        text = text[0]
        language_id = clean_parentPost_table_pipeline.get_language(text)
        language_array.append(language_id)

    plt.hist(language_array, 100, normed=1, facecolor='green', alpha=0.75)
    plt.show()

def histogram_document_length():
    '''
    Create an array of document lengths and plot them.
    [only including parentPost for now] 2/21/16
    :return:
    '''
    c =  conn.cursor()
    c.execute("SELECT selftext FROM ParentPostDetails")

    document_lengths = []
    for x in range(1000):
        text = c.fetchone()
        if(text==None or text[0]=="[deleted]" or text[0]=="[removed]"):
            print('skip')
        else:
            size = len(text[0])
            document_lengths.append(size)

    plt.hist(document_lengths, 10, normed=1, facecolor='green', alpha=0.75)
    plt.show()

def histogram_number_of_comments():
    c =  conn.cursor()
    c.execute("SELECT DISTINCT link_id FROM ParentPostDetails")

    comment_counts = []
    for x in range(1000):
        link_id = c.fetchone()
        link_id = link_id[0]
        c2 = conn.cursor()
        c2.execute("SELECT COUNT(*) FROM ParentPostDetails WHERE link_id = " + link_id)
        comment_count = c2.fetchone()
        comment_counts.append(comment_count)

    plt.hist(comment_counts, 10, normed=1, facecolor='green', alpha=0.75)
    plt.show()


if __name__ == '__main__':
   # data = clean_graphing_data()
   #histogram_document_length()
   data_stats()
  # histogram_of_languages()