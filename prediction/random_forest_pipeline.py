"""
Naive Bayes Pipeline for How to Win at Reddit
Created by Jeet Nagda
"""
from time import time

import numpy as np
from nltk.corpus import stopwords
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.grid_search import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from prediction.reporting import report
from text_pipeline import produce_timed_reddit_data as rd


def rf_pipeline(time_limit=300):
    from sklearn.ensemble import RandomForestClassifier
    print("GETTING THE DATA WITH CUTOFF TIME: " + str(time_limit))
    print("...")
    X, y = rd.get_training_data(time_limit)
    # print("PERCENT OF 0s:",y.count(0)/len(y)) # DEBUG
    print("FETCHED THE DATA")
    reddit_clf_randomForest = Pipeline([
        ('vect', CountVectorizer(stop_words=stopwords.words('english'))),
        ('tfidf', TfidfTransformer()),
        ('clf', RandomForestClassifier(class_weight='balanced')),
    ])
    print("DOING BLANK RANDOM FORESET")
    scores = cross_val_score(reddit_clf_randomForest, X, y, cv=5, scoring='roc_auc', verbose=1)
    print("NO PARAM RandomForest CLF")
    print(scores.mean())
    print("--------------------")
    param_grid = {
        "clf__n_estimators": [200, 300, 400],
        "clf__max_depth": [5, None],
        "clf__max_features": [1, 3, 10],
        "clf__min_samples_split": [1, 3, 10],
        "clf__min_samples_leaf": [1, 3, 10],
        "clf__bootstrap": [True, False],
        'tfidf__use_idf': [True, False],
        "clf__criterion": ["gini", "entropy"],
        'vect__max_df': [0.5, 0.75, 1.0],
        'vect__max_features': (None, 5000, 10000, 50000)
    }
    print("STARTING TO TRAIN")
    start = time()
    n_iter_search = 5
    rs_clf = RandomizedSearchCV(reddit_clf_randomForest, param_distributions=param_grid, n_iter=n_iter_search,
                                n_jobs=-1, verbose=1, cv=5, scoring='roc_auc')
    rs_clf.fit(X, y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    # best = report(rs_clf.grid_scores_, 5)
    return report(rs_clf.grid_scores_, 5)


if __name__ == '__main__':
    print("Random Forest Pipeline")
    cutoff_times_to_test = [1]
    score = []
    for cutoff_time in cutoff_times_to_test:
        print("TESETING CUTOFF TIME", cutoff_time)
        score.append(rf_pipeline())
    print(score)
    print("BEST CUTOFF TIME:", cutoff_times_to_test[np.argmax(score)])
