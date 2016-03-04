import numpy as np
import matplotlib.pyplot as  plt
import mysql_manager
import sql_manager
import clean_parentPost_table_pipeline
import text_clean_test



### create a histogram of the languages in the database
### create a histogram of the size of each mainPost
### create a histogram of the size of the number of children (comments and subcomments)
###     that one mainPost has

conn = mysql_manager.cnx
conn_lite = sql_manager.open_db_connection(sql_manager.joc_path)


def removed_comments():
    ## dont run this, takes a while. Answer is 3,138,736
    c =  conn_lite.cursor()
    c.execute("SELECT COUNT(*) FROM May2015 WHERE body = '[removed]' or body = '[deleted]'")
    print(c.fetchone())


def data_stats():

    #MySQL data
    c =  conn.cursor()
    c.execute("SELECT COUNT(*) FROM ParentPostDetails")
    size = c.fetchone()
    print("MySQL DB size: " + str(size[0]))
    c.execute('SHOW COLUMNS FROM ParentPostDetails')
    for post in c.fetchall():
        print(post)


    #sqlite3 data
    c_lite = conn_lite.cursor()
    c_lite.execute("SELECT COUNT(*) FROM May2015")
    size = c_lite.fetchone()
    print("sqlite3 DB size: " + str(size[0]))
    c_lite.execute('PRAGMA table_info(May2015);')
    for post in c_lite.fetchall():
        print(post)



def histogram_of_languages():
    c =  conn_lite.cursor()
    c.execute("SELECT body FROM May2015 LIMIT 2000")
    language_dict = {}

    for x in range(2000):
        print(x)
        text = c.fetchone()
        if(text==None or text[0]=='[removed]'or text[0]==['deleted'] or text[0] == '' or text[0].startswith("http") or text[0].startswith(";") or text[0].startswith(":") or text[0].startswith("3")):
            print('skip')
        else:
            text = text[0]
            print(text)
            language_id = clean_parentPost_table_pipeline.get_language(text)
            print(language_id)
            if(language_id not in language_dict):
                language_dict[language_id] = 1
            else:
                language_dict[language_id] = language_dict.get(language_id) + 1

    print(language_dict)

    plt.bar(range(len(language_dict)), language_dict.values(), align='center')
    plt.xticks(range(len(language_dict)), language_dict.keys())
    plt.show()


def histogram_document_length():
    '''
    Create an array of document lengths and plot them.
    [only including parentPost for now] 2/21/16
    :return:
    '''
    c =  conn_lite.cursor()
    c.execute("SELECT body FROM May2015 LIMIT 1000")

    document_lengths_dict = {}
    for x in range(1000):
        text = c.fetchone()
        if(text==None or text[0]=="[deleted]" or text[0]=="[removed]"):
            print('skip')
        else:
            size = len(text[0])
            if(size <=20):
                if('0-20 words' not in document_lengths_dict):
                    document_lengths_dict['0-20 words'] = 1
                else:
                    document_lengths_dict['0-20 words'] = document_lengths_dict.get('0-20 words') + 1
            elif(size >=21 and size <=100):
                if('21-100 words' not in document_lengths_dict):
                    document_lengths_dict['21-100 words'] = 1
                else:
                    document_lengths_dict['21-100 words'] = document_lengths_dict.get('21-100 words') + 1
            elif(size >=101 and size <=500):
                if('101-500 words' not in document_lengths_dict):
                    document_lengths_dict['101-500 words'] = 1
                else:
                    document_lengths_dict['101-500 words'] = document_lengths_dict.get('101-500 words') + 1
            elif(size >=501):
                if('500+ words' not in document_lengths_dict):
                    document_lengths_dict['500+ words'] = 1
                else:
                    document_lengths_dict['500+ words'] = document_lengths_dict.get('500+ words') + 1

    print(document_lengths_dict)

    plt.bar(range(len(document_lengths_dict)), document_lengths_dict.values(), align='center')
    plt.xticks(range(len(document_lengths_dict)), document_lengths_dict.keys())
    plt.show()


def histogram_number_of_comments():

    c = conn_lite.cursor()
    c.execute("SELECT DISTINCT link_id FROM May2015 LIMIT 1000")

    counts_dict = {}
    for x in range(1000):
        link_id = c.fetchone()
        link_id = link_id[0]
        c2 = conn_lite.cursor()
        c2.execute("SELECT COUNT(*) FROM May2015 WHERE link_id = '" + link_id + "'")
        comment_count = c2.fetchone()
        comment_count = comment_count[0]
        print(comment_count)

        if(comment_count <=10):
            if('0-5 comments' not in counts_dict):
                counts_dict['0-5 comments'] = 1
            else:
                counts_dict['0-5 comments'] = counts_dict.get('0-5 comments') + 1
        elif(comment_count >=11 and comment_count <=30):
            if('6-30 comments' not in counts_dict):
                counts_dict['6-30 comments'] = 1
            else:
                counts_dict['6-30 comments'] = counts_dict.get('6-30 comments') + 1
        elif(comment_count >=31):
            if('30+ comments' not in counts_dict):
                counts_dict['30+ comments'] = 1
            else:
                counts_dict['30+ comments'] = counts_dict.get('30+ comments') + 1



    plt.bar(range(len(counts_dict)), counts_dict.values(), align='center')
    plt.xticks(range(len(counts_dict)), counts_dict.keys())
    plt.show()



if __name__ == '__main__':
   #data_stats()
   histogram_of_languages()
  # removed_comments()
  # histogram_number_of_comments()
   #histogram_document_length()

