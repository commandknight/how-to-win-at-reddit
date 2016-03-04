"""
This piepline will be the file where we create, train and evaluate the random forest classifiers
"""
from operator import itemgetter
from time import time

import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.grid_search import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from text_pipeline import produce_timed_reddit_data as rd


def rf_pipeline():
    from sklearn.ensemble import RandomForestClassifier
    print("GETTING THE DATA")
    X, y = rd.get_training_data()
    print("FETCHED THE DATA")
    reddit_clf_randomForest = Pipeline([('vect', CountVectorizer(stop_words=stopwords.words('english'))),
                                        ('tfidf', TfidfTransformer()),
                                        ('clf', RandomForestClassifier(class_weight='balanced')),
                                        ])
    param_grid = {
        "clf__n_estimators": [100, 200, 300],
        "clf__max_depth": [3, 5, None],
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
    n_iter_search = 10
    rs_clf = RandomizedSearchCV(reddit_clf_randomForest, param_distributions=param_grid, n_iter=n_iter_search,
                                n_jobs=-1, verbose=1, cv=3, scoring='roc_auc')
    rs_clf.fit(X, y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    report(rs_clf.grid_scores_)
    # print("PERCENT OF 0s:",y.count(0)/len(y))


def report(grid_scores, n_top=3):
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
            score.mean_validation_score,
            np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")


if __name__ == '__main__':
    scores = rf_pipeline()
