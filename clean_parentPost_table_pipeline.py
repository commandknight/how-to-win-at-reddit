##############################################
### CS-175 - How To Win At Reddit
### Jocelyne Perez, Timothie Fujita, Jeet Nagda
###
### CLEAN DATA PIPELINE
###     1) is_english()
###     2) clean_parentPost_table_pipeline()
##############################################


# Make sure to pip install all packages if you're going to run this module.

import goslate
import sqlite3
import re
from langdetect import detect
import mysql.connector
import json

config = {
    'user': 'jeet',
    'password': 'paper2mate',
    'host': 'cs175redditproject.cxayrrely1fe.us-west-2.rds.amazonaws.com',
    'database': 'cs175reddit',
    'raise_on_warnings': True,
}

conn = mysql.connector.connect(**config)

# Make data global
#joc_path = '/Users/Jocelyne/Desktop/CS175/Reddit_Comments/database.sqlite'
#conn = sqlite3.connect(joc_path)


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
    ##gs = goslate.Goslate()
    ##language_id = gs.detect(text)
    print(text)
    language_id = detect(text);
    if language_id == 'en':
        return True
    return False



def remove_chars(text):
    '''
    Removes unecesary characters so that the function
    is_english(text) can run correctly without being confused
    when seeing confusing chars (',) at begining of the sentence.
    Note: this will not be used when bagging the text
    '''
    # need to figure out which chars we will remove
    text = re.sub('#[()\'",]', '',text)
    return text

#comment

def clean_parentPost_table_pipeline():
    '''
    For every parentPost, delete any post that is [removed] or [deleted]
    comment that is not in english or is [DELETED]
    '''
    c = conn.cursor()
    c.execute('SELECT selftext FROM ParentPostDetails LIMIT 10')
    
    for text in c.fetchall():
        #text = json.loads(text[0])
        print(text)
        if(text == "[deleted]" or text == "[removed]"):
             print('deleted')
        else:
             print(is_english(text))
        
