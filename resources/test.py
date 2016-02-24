import mysql.connector

# conda install -c https://conda.anaconda.org/anaconda mysql-connector-python


config = {
    'user': 'jeet',
    'password': 'paper2mate',
    'host': 'cs175redditproject.cxayrrely1fe.us-west-2.rds.amazonaws.com',
    'database': 'cs175reddit',
    'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

query = ("SELECT childrenComments FROM ParentPostDetails WHERE parentPost_id = \'t3_18h75c\' LIMIT 10")

cursor.execute(query)

for (id_test) in cursor:
    print(id_test[0])

cursor.close()
cnx.close()
