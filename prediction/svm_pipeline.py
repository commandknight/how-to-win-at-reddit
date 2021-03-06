"""
Naive Bayes Pipeline for How to Win at Reddit
Created by Jocelyne Perez
"""
from time import time

import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords
from sklearn import svm
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.grid_search import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from prediction.reporting import report
from text_pipeline import produce_timed_reddit_data as rd


def svm_pipeline(time_limit=300):
    print("GETTING THE DATA")
    print("...")
    import json
    with open('/Users/jnagda/PycharmProjects/how-to-win-at-reddit/text_pipeline/data100.json') as data_file:
        data = json.load(data_file)
    X, y = data[0], data[1]
    # X, y = rd.get_training_data(time_limit)
    print("FETCHED THE DATA")
    clf_svm = Pipeline([('vect', CountVectorizer(stop_words=stopwords.words('english'))),
                        ('tfidf', TfidfTransformer()),
                        ('clf', svm.SVC(kernel='linear', verbose=1, gamma='auto', class_weight='balanced')),
                        ])
    start = time()
    scores = cross_val_score(clf_svm, X, y, cv=3, scoring='roc_auc', verbose=1, n_jobs=-1)
    print(scores)
    print(scores.mean())
    print("CrossValidation took %.2f seconds" % (time() - start))
    # kernals: one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’
    param_grid = {
        'tfidf__use_idf': [True, False],
        'clf__kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
        'vect__max_df': [0.5, 0.75, 1.0],
        'vect__max_features': (None, 5000, 10000, 50000),
        'clf__shrinking': [True, False],
        'clf__C': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.5]
    }
    print("STARTING TO TRAIN")
    start = time()
    n_iter_search = 40
    rsvm_clf = RandomizedSearchCV(clf_svm, param_distributions=param_grid, n_iter=n_iter_search,
                                  n_jobs=-1, verbose=1, cv=5, scoring='roc_auc')
    # rsvm_clf.fit(X, y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    report(rsvm_clf.grid_scores_, 5)


def svm_pipeline2():
    print("Running svm_pipeline")
    print("GETTING THE DATA")
    print("...")
    X, y = rd.get_training_data()
    print("FETCHED THE DATA")
    # figure number for plots
    fignum = 1

    # fit the model
    for name, penalty in (('unreg', 1), ('reg', 0.05)):
        clf = svm.SVC(kernel='linear', C=penalty)
        print(clf);
       # clf.fit(X, Y)
        # get the separating hyperplane
        w = clf.coef_[0]
        a = -w[0] / w[1]
        xs = np.linspace(-5, 5)
        ys = a * xs - (clf.intercept_[0]) / w[1]

        # plot the parallels to the separating hyperplane that pass through the
        # support vectors
        margin = 1 / np.sqrt(np.sum(clf.coef_ ** 2))
        ys_down = ys + a * margin
        ys_up = ys - a * margin

        # plot the line, the points, and the nearest vectors to the plane
        plt.figure(fignum, figsize=(4, 3))
        plt.clf()
        plt.plot(xs, ys, 'k-')
        plt.plot(xs, ys_down, 'k--')
        plt.plot(xs, ys_up, 'k--')

        plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80,
                    facecolors='none', zorder=10)
        plt.scatter(X[:, 0], X[:, 1], c=y, zorder=10, cmap=plt.cm.Paired)

        plt.axis('tight')
        x_min = -4.8
        x_max = 4.2
        y_min = -6
        y_max = 6

        XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
        Z = clf.predict(np.c_[XX.ravel(), YY.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(XX.shape)
        plt.figure(fignum, figsize=(4, 3))
        plt.pcolormesh(XX, YY, Z, cmap=plt.cm.Paired)

        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

        plt.xticks(())
        plt.yticks(())
        fignum = fignum + 1

    plt.show()


if __name__ == '__main__':
    svm_pipeline()
    # svm_pipeline2()
