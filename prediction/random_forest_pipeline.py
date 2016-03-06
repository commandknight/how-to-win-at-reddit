"""
This piepline will be the file where we create, train and evaluate the random forest classifiers
JEET
"""

from time import time

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.grid_search import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from prediction.reporting import report
from text_pipeline import produce_timed_reddit_data as rd


# TODO: Comment this code

def rf_pipeline():
    from sklearn.ensemble import RandomForestClassifier
    print("GETTING THE DATA")
    print("...")
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
    n_iter_search = 30
    rs_clf = RandomizedSearchCV(reddit_clf_randomForest, param_distributions=param_grid, n_iter=n_iter_search,
                                n_jobs=-1, verbose=1, cv=5, scoring='roc_auc')
    rs_clf.fit(X, y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    report(rs_clf.grid_scores_, 5)
    # print("PERCENT OF 0s:",y.count(0)/len(y))


if __name__ == '__main__':
    scores = rf_pipeline()