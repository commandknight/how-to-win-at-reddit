from nltk import word_tokenize
from nltk.stem import PorterStemmer


class PorterTokenizer(object):
    """
    This object was created by example in Scikitlearn
    It uses the NLTK Tokenizer and the NLTK Porter Stemmer to create a PorterTokenizer usable in CountVectorizer
    """
    def __init__(self):
        self.ps = PorterStemmer()

    def __call__(self, doc):
        return [self.ps.stem(t) for t in word_tokenize(doc)]
