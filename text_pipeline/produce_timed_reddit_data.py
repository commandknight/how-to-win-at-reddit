"""
Product Timed Reddit Data
- Pulls all available Reddit post data from MySQL DB
- Pull matching comment data for Reddit posts from SQLite
- Label post as popular or unpopular based on post score
- Return as training data and target data
"""

from sklearn.utils import shuffle

from text_pipeline import comment_db_manager as cdm
from text_pipeline import mysql_manager
from text_pipeline import serialize_comments as sc

def get_avg_scores_by_subreddit():
    import csv
    avg_score_subreddit = {}
    with open('/Users/jnagda/PycharmProjects/how-to-win-at-reddit/resources/avg_scores_by_subreddit.csv',
              'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for row in csvreader:
            avg_score_subreddit[row[0]] = float(row[1])
    return avg_score_subreddit


def get_training_data(time_limit=600):
    """
    Categorize all available data for use in all classification pipelines
    :param time_limit: In minutes. Number of minutes after parent post is created to define "warm" posts.
    :return: Tuple of training data and target data
    """
    all_records = mysql_manager.get_parent_post_data()
    all_records = [all_records[0]]
    training_data = []
    target_data = []
    avg_score_subreddit = get_avg_scores_by_subreddit()
    error = 0
    for parentPost_id, childrenComments, score, url, selftext, timecreated_utc, subreddit, title, author in all_records:
        print(parentPost_id)
        if '[removed]' not in selftext and '[deleted]' not in selftext:
            post_text = url + selftext
        else:
            post_text = url
        print("POST TEXT", post_text)
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
        print("CHILDREN TEXT", children_text)
        training_data.append(post_text + children_text + title)
        print("FINAL TEXT", post_text + children_text + title)
        target_data.append(1 if float(score) > avg_score_subreddit[subreddit] else 0)
    if error > 0:
        print("Total errors in getting time_cut_off data: " + str(error))
    # print("Length of target: ", len(target_data)) #DEBUG
    return shuffle(training_data, target_data)


if __name__ == "__main__":
    test = get_training_data()
    print(len(test[0]))
    # import json
    # with open('data.txt', 'w') as outfile:
    #     json.dump(test, outfile)
