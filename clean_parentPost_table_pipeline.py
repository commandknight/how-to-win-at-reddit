##############################################
### CS-175 - How To Win At Reddit
### Jocelyne Perez, Timothie Fujita, Jeet Nagda
###
### CLEAN DATA PIPELINE
###     1) is_english()
###     2) clean_parentPost_table_pipeline()
##############################################


# Make sure to pip install all packages if you're going to run this module.

import sqlite3
import re
from langdetect import detect
import mysql_manager


config = mysql_manager.config
joc_path = '/Users/Jocelyne/Desktop/CS175/Reddit_Comments/database.sqlite'
conn = mysql.connector.connect(**config)

def get_unique_parent_ids():
    '''
    Function that returns list of unique link_IDs
    :return: list of strings (ids)
    '''
    c = conn.cursor()
    #c.execute('SELECT DISTINCT * FROM ParentPostDetails LIMIT 20')
    c.execute('SHOW COLUMNS FROM ParentPostDetails')
    for post in c.fetchall():
        print(post)
   # return c.fetchall()


    
def is_english(text):
    '''
    Uses (free) Google Translate API to detect the language
    the language is in. Returns True if it's in english;
    False otherwise
    '''    
    language_id = detect(text)
    if language_id == 'en':
        return True
    return False



def remove_chars(mystring):
    '''
    Removes unecesary characters so that the function
    is_english(text) can run correctly without being confused
    when seeing confusing chars (',) at begining of the sentence.
    Note: this will not be used when bagging the text
    '''
    # need to figure out which chars we will remove
    re.sub('[^A-Za-z0-9]+', '', mystring)
    return mystring

#comment

def clean_parentPost_table_pipeline():
    '''
    For every parentPost, delete any post that is [removed] or [deleted]
    comment that is not in english or is [DELETED]
    '''
    c = conn.cursor()
    c.execute('SELECT selftext FROM ParentPostDetails LIMIT 10')

    for text in c.fetchall():
        text = text[0]
        if(text == "[deleted]" or text == "[removed]"):
            print('deleted') #not deleting from DB yet, but will once all files are up and running
        elif (text==""):
            print("check to see that other fields are filled in")
        else:
            print(is_english(text))



        
if __name__ == '__main__':
    print("Beggining clean_parentPost_table_pipeline...\n\n")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM ParentPostDetails")
    print(c.fetchone())
