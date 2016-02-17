import mysql.connector

config = {
    'user': 'jeet',
    'password': 'paper2mate',
    'host': 'cs175redditproject.cxayrrely1fe.us-west-2.rds.amazonaws.com',
    'database': 'cs175reddit',
    'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)

add_parentPostDetail = ("INSERT INTO ParentPostDetails "
                        "(parentPost_id,url,timecreated_utc,subreddit_id,subreddit,title,score,author) "
                        "VALUES (%(id)s, %(url)s, %(timecreated)s, %(subreddit_id)s, %(subreddit)s, %(title)s, %(score)s, %(author)s)")


# DEBUG FUNCTION DELETE ME LATER
def print_all_testTable():
    curr = cnx.cursor()
    query = ("SELECT * FROM testTable")
    curr.execute(query)
    for x in curr:
        print(x[0])
    curr.close()


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
    print(parentDict)
    try:
        curr.execute(add_parentPostDetail, parentDict)
    except:
        print("ERROR in inserting: " + str(curr.statement))
    cnx.commit()
    curr.close()


def close_connection():
    cnx.close()
