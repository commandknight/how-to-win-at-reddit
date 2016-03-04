import mysql.connector

from text_pipeline import serialize_comments as sc

"""
config = {
    'user': 'jeet',
    'password': 'paper2mate',
    'host': 'cs175redditproject.cxayrrely1fe.us-west-2.rds.amazonaws.com',
    'database': 'cs175reddit',
    # 'cursorclass' : 'MySQLdb.cursors.SSCursor',
    'raise_on_warnings': True
}
"""

config = {
    'user': 'root',
    'password': 'CS122Bsql',
    'host': 'localhost',
    'database': 'cs175reddit',
    'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

add_parentPostDetail = ("INSERT IGNORE INTO ParentPostDetails "
                        "(parentPost_id,url,timecreated_utc,subreddit_id,subreddit,title,score,author,selftext) "
                        "VALUES (%(id)s, %(url)s, %(timecreated)s, %(subreddit_id)s, %(subreddit)s, %(title)s, %(score)s, %(author)s, %(selftext)s)")

update_parentPost_child_ids = "UPDATE ParentPostDetails SET childrenComments=%s WHERE parentPost_id=%s "

get_parent_data_sql = "SELECT parentPost_id,childrenComments,score,url,selftext,timecreated_utc FROM ParentPostDetails"

get_parent_created_sql = "SELECT parentPost_id, timecreated_utc FROM ParentPostDetails WHERE parentPost_id = %s"

get_parent_post_ids_sql = "SELECT parentPost_id FROM ParentPostDetails"


# PLEASE DONT USE THIS METHOD, BAD PRACTICE!
def perform_query(query):
    """
    Method to perform RAW Sql Query and return cursor result list
    :param query: SQL String to execute
    :return: Cursor.fetchall() result list is returned
    """
    curr = cnx.cursor()
    curr.execute(query)
    return curr.fetchall()


def create_cursor():
    return cnx.cursor()


"""
def perform_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()
"""

# TODO: Add Limit clause that is optional?
def get_parent_post_data():
    """
    Method to get the text related features of parent_post_details, including ChildrenID list
    NOTE, this method may hang, in that case, run again? Jeet is working on more stable
    :return: list from Cursor for all ParentPostDetail records
    """
    curr = cnx.cursor()
    curr.execute(get_parent_data_sql)
    result = []
    x = 0
    for y in curr:
        print("ITER", x)
        result.append(y)
        x += 1
    curr.close()
    return result


def get_parent_post_ids():
    curr = cnx.cursor()
    curr.execute(get_parent_post_ids_sql)
    result = curr.fetchall()
    curr.close()
    return result


def update_parentPost(child_ids, parentPost_id):
    """
    Method to update the ParentPosDetails with list of children IDs stored as a BLOB
    :param child_ids: list of strings for IDs of children comments
    :param parentPost_id: id of the record to update in ParentPostDetails
    :return:
    """
    curr = cnx.cursor()
    child_ids_serialized = sc.serialize_list(child_ids)
    try:
        curr.execute(update_parentPost_child_ids, (child_ids_serialized, parentPost_id))
    except:
        print("ERROR in updating with children ids: " + str(curr.statement))
    cnx.commit()
    curr.close()


""" DEPRECATED: NOT USING THIS FUNCTION, USE insert_parentdetails_BIG(list_of_dicts) """
def insert_parent_dict_into_parentPostDetail(parent_id, parent_info):
    if parent_info is None: return
    curr = cnx.cursor()
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


def insert_parentdetails_BIG(list_of_dicts):
    """
    Function to insert a list of parent post dictionaries into the mysql database ParentPostTable
    :param list_of_dicts: list of dictionaries for parentPost record to insert
    :return:
    """
    curr = cnx.cursor()
    # curr.executemany(add_parentPostDetail,list_of_dicts)
    for record in list_of_dicts:
        print("ADDING: ", record['id'])
        try:
            curr.execute(add_parentPostDetail, record)
        except:
            print("ERROR ADDING", record['id'])
    cnx.commit()
    curr.close()


def get_parent_created_info(parent_id):
    db_cursor = cnx.cursor()
    db_cursor.execute(get_parent_created_sql, (parent_id,))
    result = db_cursor.fetchone()
    db_cursor.close()
    return result


def close_connection():
    """
    Function to close connection to MySQL Database
    :return: None
    """
    cnx.close()
