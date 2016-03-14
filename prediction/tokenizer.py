from nltk import word_tokenize
from nltk.stem import PorterStemmer


class PorterTokenizer(object):
    def __init__(self):
        self.ps = PorterStemmer()

    def __call__(self, doc):
        return [self.ps.stem(t) for t in word_tokenize(doc)]
