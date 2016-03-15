"""
Naive Bayes Pipeline for How to Win at Reddit
Created by Timothie Fujita
"""
from time import time

from nltk.corpus import stopwords
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.grid_search import RandomizedSearchCV
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline

from prediction.tokenizer import PorterTokenizer
from prediction.reporting import report
from text_pipeline import produce_timed_reddit_data as rd


def bernoulli_nb_pipeline(time_limit=300):
    print("GETTING THE DATA")
    print("...")
    X, y = rd.get_training_data(time_limit)
    print("FETCHED THE DATA")
    text_bernNB = Pipeline([('vect', CountVectorizer(tokenizer=PorterTokenizer(), stop_words=stopwords.words('english'))),
                            ('tfidf', TfidfTransformer()),
                            ('clf', BernoulliNB()),
                            ])
    print('Blank clf')
    scores = cross_val_score(text_bernNB, X, y, cv=5, scoring='roc_auc',verbose=1,n_jobs=-1)
    print("NO PARAM BernouliNB CLF")
    print(scores.mean())
    print("--------------------")
    param_grid = {
        "clf__alpha": [0.1, 0.5, 0.7, 0.8, 1.0, 1.2],
        "clf__binarize": [0.0, 0.01, 0.025, 0.05, 0.1, 0.2, 0.5],
        "clf__fit_prior": [True, False],
        'tfidf__use_idf': [True, False],
        'vect__max_df': [0.5, 0.75, 1.0],
        'vect__max_features': (None, 5000, 10000, 50000)
    }
    print("STARTING TO TRAIN")
    start = time()
    n_iter_search = 30
    rbernNB_clf = RandomizedSearchCV(text_bernNB, param_distributions=param_grid, n_iter=n_iter_search,
                                     n_jobs=-1, verbose=1, cv=5, scoring='roc_auc')
    rbernNB_clf.fit(X, y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    report(rbernNB_clf.grid_scores_, 30)


if __name__ == '__main__':
    print("Naive Bayes Pipeline")
    bernoulli_nb_pipeline()
