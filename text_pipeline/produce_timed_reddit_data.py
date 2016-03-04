"""
Product Timed Reddit Data
- Pulls all available Reddit post data from MySQL DB
- Pull matching comment data for Reddit posts from SQLite
- Label post as popular or unpopular based on post score
- Return as training data and target data
"""

from text_pipeline import serialize_comments as sc

def get_training_data(time_limit=300):
    """
    Categorize all available data for use in all classification pipelines
    :param time_limit: In minutes. Number of minutes after parent post is created to define "warm" posts.
    :return: Tuple of training data and target data
    """
    from text_pipeline import mysql_manager
    all_records = mysql_manager.get_parent_post_data()
    mysql_manager.close_connection()
    from text_pipeline import comment_db_manager as cdm
    training_data = []
    target_data = [1 if record[2] > 302 else 0 for record in all_records]
    # print("Length of target: ", len(target_data)) #DEBUG
    error = 0
    for parentPost_id, childrenComments, score, url, selftext, timecreated_utc in all_records:
        post_text = url + selftext
        children_text = ""
        try:
            list_of_comments = []
            unserialized_children = sc.deserialize_list(childrenComments)
            list_of_comments = cdm.get_children_comments_timed(timecreated_utc, unserialized_children, time_limit)
        except:
            print("ERROR WITH " + parentPost_id)
            error += 1
        if len(list_of_comments) > 0:
            for comment_id in list_of_comments:
                children_text += cdm.get_children_text_features(comment_id)
        training_data.append(post_text + children_text)
    cdm.close_db_connection()
    print("Total errors: " + str(error))
    return training_data, target_data