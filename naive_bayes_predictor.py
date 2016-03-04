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
from text_pipeline import produce_timed_reddit_data as rd


def bernoulli_nb_pipeline():

    X, y = rd.get_training_data()
    text_bernNB = Pipeline([('vect', CountVectorizer(stop_words=stopwords.words('english'))),
                            ('tfidf', TfidfTransformer()),
                            ('clf', BernoulliNB(binarize=0.5)),
                            ])
    scores = cross_val_score(text_bernNB, X, y, cv=5, n_jobs=-1, scoring='accuracy')
    return scores


if __name__ == '__main__':
    print("Naive Bayes Pipeline")
    scores = bernoulli_nb_pipeline()
    print(scores)
    print(scores.mean())