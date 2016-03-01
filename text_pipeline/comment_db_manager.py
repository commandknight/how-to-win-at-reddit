import sqlite3

jeet_path = '/Users/jnagda/Documents/Reddit_Comments/database.sqlite'
timothie_path = 'C:/Users/Timothie/Desktop/reddit-comments-may-2015/database.sqlite'
timothie_desktop = 'E:/Downloads/reddit-comments-may-2015/database.sqlite'
conn = sqlite3.connect(timothie_path)

sql_statement_children = "SELECT body,author FROM May2015 WHERE id = ?"

sql_get_children = 'SELECT id, parent_id, link_id, created_utc FROM May2015 WHERE link_id = ?'

sql_get_child = 'SELECT id, created_utc FROM May2015 WHERE id = ?'

def open_db_connection(path):
    """
    Open the db connection to the local machine
    :param path: Path of local db
    """
    conn = sqlite3.connect(path)
    return conn


def get_children_text_features(comment_id):
    """
    Function to get all the text features as a string from a single comment ID
    :param comment_id: ID of the child comment to get
    :return: String of the comment text features: body & author
    """
    db_curr = conn.cursor()
    db_curr.execute(sql_statement_children, (comment_id,))
    result = db_curr.fetchone()
    db_curr.close()
    return str(result[0]) + str(result[1])


def get_children_comments(parentID):
    """
    Function to get all the comments IDs, and created_utc of a given parentID
    :param parentID: the link_id of the comments to get
    :return: list of (id,parent_id,link_id,created_utc)
    """
    db_curr = conn.cursor()
    db_curr.execute(sql_get_children, (parentID,))
    result = db_curr.fetchall()
    db_curr.close()
    return result


def get_children_comments_timed(parent_created_time, children_ids, time_limit):
    """
    Given list of children, prune children comments which do not fit within timeline
    :param parent_created_time: Time when parent post was created in epoch time (seconds)
    :param children_ids: List of children IDs
    :param time_limit: Time limit from parent post time in MINUTES
    :return: Return children ids posted within time limit
    """
    pruned_children = []
    cutoff_time = parent_created_time + (time_limit * 60)
    db_curr = conn.cursor()

    for x in children_ids:
        result = db_curr.execute(sql_get_child, (x, ))

        # Only allow comments which fall within the parent post / time limit
        for c_id, time in result:
            if parent_created_time <= time <= cutoff_time:
                pruned_children.append(c_id)

    db_curr.close()
    return pruned_children


def get_unique_parent_ids():
    """
    Function that returns list of unique link_IDs
    :return: list of tuples (link_ids {string},subreddit {string})
    """
    conn = sqlite3.connect(jeet_path)
    curr = conn.cursor()
    print("getting ids")
    curr.execute(
        'SELECT DISTINCT link_id,subreddit FROM May2015 WHERE subreddit != \'promos\' AND link_id = parent_id LIMIT 500 OFFSET 5060')
    return curr.fetchall()


# Please Dont use this function, bad practice!
def perform_query(path, query):
    # conn = sqlite3.connect(path)
    conn = sqlite3.connect(jeet_path)
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()


def get_test_data(path):
    """
    Returns first 10 rows of May2015 table as a sample test
    :param path: path to connect SQLiteDB
    :return: cursor to first 10 rows
    """
    conn = sqlite3.connect(path)
    result = conn.execute('SELECT * FROM May2015 LIMIT 5')
    return result


def close_db_connection():
    """
    Function to close the DB Connection
    :return: None
    """
    conn.close()
