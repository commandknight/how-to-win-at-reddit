"""
Naive Bayes Pipeline for How to Win at Reddit

- Naive Bayes Pipeline
    - Naive Bayes Classifier
    - Cross Validation
    - Get Text and Prepare
"""
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
from text_pipeline import serialize_comments as sc

def get_training_data():
    from text_pipeline import mysql_manager
    print("getting data!")
    all_records = mysql_manager.get_parent_post_data()
    print("Got data")
    mysql_manager.close_connection()
    print("LEN",len(all_records))
    from text_pipeline import comment_db_manager as cdm
    training_data = []
    target_data = [1 if record[2] > 414 else 0 for record in all_records]
    print("LEN OF TARGET", len(target_data))
    for parentPost_id, childrenComments, score, url, selftext, timecreated_utc in all_records:
        post_text = url + selftext
        children_text = ""
        #list_of_comments = cdm.get_children_comments_timed(timecreated_utc, cdm.get_children_comments(parentPost_id), 300)
        try:
            list_of_comments = sc.deserialize_list(childrenComments)
        except:
            print("ERROR WITH " + parentPost_id)
        for comment_id in list_of_comments:
            children_text += cdm.get_children_text_features(comment_id)
        training_data.append(post_text + children_text)
        print(post_text + children_text)
    cdm.close_db_connection()
    print("Training data collected" + training_data)
    print("Target data collected" + target_data)
    return training_data, target_data


def bernoulli_nb_pipeline():

    X, y = get_training_data()
    text_bernNB = Pipeline([('vect', CountVectorizer(stop_words=stopwords.words('english'))),
                            ('tfidf', TfidfTransformer()),
                            ('clf', BernoulliNB(binarize=0)),
                            ])
    scores = cross_val_score(text_bernNB, X, y, cv=5, n_jobs=-1, scoring='accuracy')
    return scores


if __name__ == '__main__':
    print("Naive Bayes Pipeline")
    scores = bernoulli_nb_pipeline()
    print(scores)
    print(scores.mean())