import sqlite3

jeet_path = '/Users/jnagda/Documents/Reddit_Comments/database.sqlite'
timothie_path = 'C:/Users/Timothie/Desktop/reddit-comments-may-2015/database.sqlite'
timothie_desktop = 'E:/Downloads/reddit-comments-may-2015/database.sqlite'
conn = sqlite3.connect(jeet_path)

sql_statement_children = "SELECT body,author FROM May2015 WHERE id = ?"


def open_db_connection(path):
    """
    Open the db connection to the local machine
    :param path: Path of local db
    """
    conn = sqlite3.connect(path)


def get_children_text_features(comment_id):
    """
    Function to get all the text features as a string from a single comment ID
    :param comment_id: ID of the child comment to get
    :return: String of the comment text features: body & author
    """
    db_curr = conn.cursor()
    db_curr.execute(sql_statement_children, (comment_id,))
    result = db_curr.fetchone()
    return str(result[0]) + str(result[1])


def get_unique_parent_ids():
    """
    Function that returns list of unique link_IDs
    :return: list of tuples (link_ids {string},subreddit {string})
    """
    conn = sqlite3.connect(jeet_path)
    curr = conn.cursor()
    curr.execute(
        'SELECT DISTINCT link_id,subreddit FROM May2015 WHERE subreddit != \'promos\' AND link_id = parent_id LIMIT 500 OFFSET 3060')
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
