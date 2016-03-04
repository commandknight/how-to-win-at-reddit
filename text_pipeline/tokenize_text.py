###  This file's purpopse is to tokenize a document *note that we don't mean a file, just a string of text



def tokenize_simple(document):
    import re, string
    document = document.lower()  # convert document to lower case
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    document = regex.sub(' ', document)  # replace all punctuation marks with single spaces
    document = re.sub('\s+', ' ',
                      document).strip()  # replace one or more spaces with single space AND strip leading/trailng whitespace
    return document.split()  # return list of tokens splitting on single space


def remove_stopwords_inner(tokens, stopwords):
    stopwords = set(stopwords)
    return [x for x in tokens if x not in stopwords]

def remove_stopwords_nltk(tokens):
    from nltk.corpus import stopwords
    return remove_stopwords_inner(tokens, stopwords=stopwords.words('english'))