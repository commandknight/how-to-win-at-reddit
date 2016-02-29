"""
This piepline will be the file where we create, train and evaluate the random forest classifiers
"""
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from text_pipeline import serialize_comments as sc


def get_training_data():
    from text_pipeline import mysql_manager
    all_records = mysql_manager.get_parent_post_data()
    mysql_manager.close_connection()
    from text_pipeline import comment_db_manager as cdm
    training_data = []
    target_data = [1 if record[2] > 414 else 0 for record in all_records]
    for parentPost_id, childrenComments, score, url, selftext, timecreated_utc in all_records:
        # get_text_of_post
        post_text = url + selftext
        # get_text_of_children
        children_text = ""
        # list_of_comments = select_timecutoff(timecreated_utc,time_limit,sc.deserialize_list(childrenComments))
        try:
            list_of_comments = sc.deserialize_list(childrenComments)
        except:
            print("ERROR WITH " + parentPost_id)
        for comment_id in list_of_comments:
            children_text += cdm.get_children_text_features(comment_id)
        training_data.append(post_text + children_text)
    cdm.close_db_connection()
    return training_data, target_data


def rf_pipeline():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.cross_validation import cross_val_score
    X, y = get_training_data()
    reddit_clf_randomForest = Pipeline([('vect', CountVectorizer(stop_words=stopwords.words('english'))),
                                        ('tfidf', TfidfTransformer()),
                                        ('clf', RandomForestClassifier()),
                                        ])
    scores = cross_val_score(reddit_clf_randomForest, X, y, cv=5, n_jobs=-1, scoring='accuracy')
    return scores


if __name__ == '__main__':
    scores = rf_pipeline()
    print(scores)
    print(scores.mean())
