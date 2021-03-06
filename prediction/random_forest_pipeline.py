"""
Naive Bayes Pipeline for How to Win at Reddit
Created by Jeet Nagda
"""
from time import time

from nltk.corpus import stopwords
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.grid_search import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from prediction.reporting import report
from prediction.tokenizer import PorterTokenizer
from text_pipeline import produce_timed_reddit_data as rd


def rf_pipeline(time_limit=300):
    from sklearn.ensemble import RandomForestClassifier
    print("GETTING THE DATA WITH CUTOFF TIME: " + str(time_limit))
    print("...")
    import json
    with open('/Users/jnagda/PycharmProjects/how-to-win-at-reddit/text_pipeline/data100.json') as data_file:
        data = json.load(data_file)
    X, y = data[0], data[1]
    # X, y = rd.get_training_data(time_limit)
    print("PERCENT OF 0s (Not Popular):", y.count(0) / len(y))  # DEBUG
    print("FETCHED THE DATA")
    reddit_clf_randomForest = Pipeline([
        ('vect', CountVectorizer(tokenizer=PorterTokenizer(), stop_words=stopwords.words('english'))),
        ('tfidf', TfidfTransformer()),
        ('clf',
         RandomForestClassifier(n_estimators=50, class_weight='balanced', criterion='gini', n_jobs=-1, verbose=1)),
    ])
    print("DOING BLANK RANDOM FOREST")
    start = time()
    scores = cross_val_score(reddit_clf_randomForest, X, y, cv=3, scoring='roc_auc', verbose=1, n_jobs=-1)
    print("CrossValidation took %.2f seconds" % (time() - start))
    print("NO PARAM RandomForest CLF")
    print(scores)
    print(scores.mean())
    print("--------------------")
    param_grid = {
        # "clf__n_estimators": [50, 100, 150],
        "vect__tokenizer": [None, PorterTokenizer()],  # testing stemming or not
        # "clf__max_depth": [5, 10, 20, None], too expensive?
        "clf__max_features": [None, 1, 3, 5, 10],
        "clf__min_samples_split": [1, 3],
        # "clf__min_samples_leaf": [1, 3],
        "clf__bootstrap": [True, False],
        'tfidf__use_idf': [False],  # False is better?
        # "clf__criterion": ["gini", "entropy"],
        # 'vect__max_df': [0.5, 0.75, 1.0],
        'vect__max_features': (None, 10000, 50000)
    }
    print("STARTING TO TRAIN")
    start = time()
    n_iter_search = 10
    rs_clf = RandomizedSearchCV(reddit_clf_randomForest, param_distributions=param_grid, n_iter=n_iter_search,
                                n_jobs=-1, verbose=1, cv=3, scoring='roc_auc')
    # rs_clf.fit(X, y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    return report(rs_clf.grid_scores_, 5)


if __name__ == '__main__':
    print("Random Forest Pipeline")
    cutoff_times_to_test = [100]
    # TODO: 30, 60, 90, 100, 120, 150, 200, 300
    score = []
    for cutoff_time in cutoff_times_to_test:
        print("TESTING CUTOFF TIME", cutoff_time)
        score.append(rf_pipeline(cutoff_time))
    print(score)
