from time import time

import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.grid_search import RandomizedSearchCV
from sklearn.pipeline import Pipeline

from prediction.reporting import report
from text_pipeline import produce_timed_reddit_data as rd


# we create 40 separable points
#np.random.seed(0)
#X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]
#Y = [0] * 20 + [1] * 20



#X = CountVectorizer(stop_words=stopwords.words('english'))
#iris = datasets.load_iris()
#X = iris.data[:, [0,2]]
#Y = iris.target

    # Split into training and test data
    # Learn and classify on training data
    # Predict on test data
    # Calculate MSE on test data

# nltk sentiment analysis utls

def svm_accuracy():
    # cv = CountVectorizer(stop_words=stopwords.words('english'))
    # tfidf = TfidfTransformer()
    # print(svm.SVC(kernel='linear',C=0.05))
    print("Fetching data...")
    X, Y = rd.get_training_data()
    print("Fetched data...")
    clf_svm = Pipeline([('vect', CountVectorizer(stop_words=stopwords.words('english'))),
                        ('tfidf', TfidfTransformer()),
                        ('clf', svm.SVC(verbose=1, gamma='auto', class_weight='balanced')),
                        ])
    # kernals: one of ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’
    param_grid = {
        'tfidf__use_idf': [True, False],
        'clf__kernel': ['linear', 'poly'],
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
    rsvm_clf.fit(X, Y)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    report(rsvm_clf.grid_scores_, 5)

def svm_pipeline():
    print("Running svm_pipeline")
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
        plt.scatter(X[:, 0], X[:, 1], c=Y, zorder=10, cmap=plt.cm.Paired)

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
    svm_accuracy()
    # svm_pipeline()
   #for i in range(10):
   #    print(i, X[i])

