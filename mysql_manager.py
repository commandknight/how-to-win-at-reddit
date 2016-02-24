import mysql.connector
import serialize_comments

config = {
    'user': 'jeet',
    'password': 'paper2mate',
    'host': 'cs175redditproject.cxayrrely1fe.us-west-2.rds.amazonaws.com',
    'database': 'cs175reddit',
    'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)

add_parentPostDetail = ("INSERT IGNORE INTO ParentPostDetails "
                        "(parentPost_id,url,timecreated_utc,subreddit_id,subreddit,title,score,author,selftext) "
                        "VALUES (%(id)s, %(url)s, %(timecreated)s, %(subreddit_id)s, %(subreddit)s, %(title)s, %(score)s, %(author)s, %(selftext)s)")


update_parentPost_child_ids = ("""
                                UPDATE ParentPostDetails
                                SET childrenComments = %s
                                WHERE parentPost_id = %s
                                """)


# DEBUG FUNCTION DELETE ME LATER
def print_all_testTable():
    curr = cnx.cursor()
    query = ("SELECT * FROM testTable")
    curr.execute(query)
    for x in curr:
        print(x[0])
    curr.close()


def create_cursor():
    curr = cnx.cursor()
    return curr


def perform_query(curr, query):
    curr.execute(query)
    results = curr.fetchall()
    return results


def update_parentPost(curr, child_ids, parentPost_id):

    serialized_children = serialize_comments.serialize_list(child_ids)
    try:
        curr.execute(update_parentPost_child_ids, (serialized_children, parentPost_id))
        cnx.commit()
    except:
        cnx.rollback()
        print("error updating parent post with children ids: ")
        print(str(curr.statement))


""" DEPRECATED: NOT USING THIS FUNCTION, USE insert_parentdetails_BIG(list_of_dicts) """
def insert_parent_dict_into_parentPostDetail(parent_id, parent_info):
    if parent_info is None: return
    curr = cnx.cursor()
    # author = '[deleted]' if parent_info['author'] is None else parent_info['author'].name
    parentDict = {
        'author': '[deleted]' if parent_info['author'] is None else parent_info['author'].name,
        'id': parent_id[0],
        'url': parent_info['url'],
        'timecreated': parent_info['created'],
        'subreddit_id': parent_info['subreddit_id'],
        'subreddit': parent_info['subreddit'].display_name,
        'title': parent_info['title'],
        'score': parent_info['score']
    }
    try:
        curr.execute(add_parentPostDetail, parentDict)
    except:
        print("ERROR in inserting: " + str(curr.statement))
    cnx.commit()
    curr.close()


# Function to insert a list of parent post dictionaries into the mysql database ParentPostTable
def insert_parentdetails_BIG(list_of_dicts):
    curr = cnx.cursor()
    # curr.executemany(add_parentPostDetail,list_of_dics)
    for record in list_of_dicts:
        print("ADDING: ", record['id'])
        try:
            curr.execute(add_parentPostDetail, record)
        except:
            print("ERROR ADDING", record['id'])
    cnx.commit()
    curr.close()


# Function to close database connection
def close_connection(curr):
    curr.close()
    cnx.close()
