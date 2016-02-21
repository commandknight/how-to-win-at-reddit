import mysql_manager
import serialize_comments
import sql_manager

sql_statement = "SELECT childrenComments FROM ParentPostDetails WHERE parentPost_id=\'t3_2lcfzp\' LIMIT 10"

sql_statement_children = "SELECT body FROM May2015 WHERE id = "


def get_all_text_from_children_comments(list_of_children):
    big_string = ""
    for child in list_of_children:
        test_string = sql_statement_children + "\'" + child + "\'"
        # print(test_string)
        t = sql_manager.perform_query('/Users/jnagda/Documents/Reddit_Comments/database.sqlite', test_string)
        # print(t[0][0])
        big_string += str(t[0][0])
    return big_string


def tokenize_simple(document):
    import re, string
    document = document.lower()  # convert document to lower case
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    document = regex.sub(' ', document)  # replace all punctuation marks with single spaces
    document = re.sub('\s+', ' ',
                      document).strip()  # replace one or more spaces with single space AND strip leading/trailng whitespace
    return document.split()  # return list of tokens splitting on single space


def remove_stopwords_inner(tokens, stopwords):
    """
    Removes stopwords from the given tokens.

    Parameters
    ----------
    tokens : Iterable[str]
        The tokens from which to remove stopwords.

    stopwords : Iterable[str]
        The tokens to remove.

    Returns
    -------
    List[str]
        The input tokens with stopwords removed.

    Example
    -------
    >>> document = load_hamlet()
    >>> tokens = tokenize_simple(document)
    >>> remove_stopwords_inner(tokens, ['of', 'to'])[:10]
    ['the', 'tragedie', 'hamlet', 'by', 'william', 'shakespeare', '1599', 'actus', 'primus', 'scoena']
    """
    # convert to a set for speed of lookup in the next step
    stopwords = set(stopwords)
    return [x for x in tokens if x not in stopwords]


def remove_stopwords_nltk(tokens):
    """
    Remove the NLTK English stopwords from the given tokens using remove_stopwords_inner.

    Parameters
    ----------
    tokens : Iterable[str]
        The tokens from which to remove stopwords.

    Returns
    -------
    List[str]
        The input tokens with NLTK's English stopwords removed.

    Example
    -------
    >>> document = load_hamlet()
    >>> tokens = tokenize_nltk(document)
    >>> tokens = remove_stopwords_nltk(tokens)
    >>> tokens[:10]
    ['[', 'tragedie', 'hamlet', 'william', 'shakespeare', '1599', ']', 'actus', 'primus', '.']
    """
    from nltk.corpus import stopwords
    return remove_stopwords_inner(tokens, stopwords=stopwords.words('english'))


def process_big_text(body_of_text):
    tokens = tokenize_simple(body_of_text)
    print(len(tokens))
    tokens = remove_stopwords_nltk(tokens)
    print(len(tokens))


def create_count_vectorizer_for_text(train_data, test_data):
    """
    Parameters
    ----------
    train_data : List[str]
        Training News data in list

    test_data : List[str]
        Test data in list
    """
    from sklearn.feature_extraction.text import CountVectorizer
    from nltk.corpus import stopwords
    count_vect = CountVectorizer(stop_words=stopwords.words('english'))
    X_train_counts = count_vect.fit_transform(train_data)
    X_test_counts = count_vect.transform(test_data)
    return X_train_counts, X_test_counts


"""
I am eating pancakes with maple syrup Just joined the bitcoin and changetip groups on reddit. This definitely helps; also, all boosts and push appreciated ;)Hello!!I am a newbie here and eagerly waiting for my free bits.How do I withdraw ? I can click the send button :/thanks it's kinda of a cool thing.Social Experiment?I made a new crypot currency trading platform... If anyone is interested in beta testing let me know. Looking for some real user feedback on what features i should junk or add. Right now it has things like multi exchange price list and each refreshes as fast as the exchange updates their price. Think I could have something here but want to make sure before I go through with it. Beta testers can keep the Beta version, after Beta only paid versions will be available.
Hello, finally trying bitcoin after hearing so much about it :) thanksI'm trying this ... Just getting back into Cryptocurrency. Free bits please?Hi! I'm new to Bitcoin does this tip bot work the same as doge?
"""

if __name__ == '__main__':
    q_results = mysql_manager.perform_query(sql_statement)
    big_string = ""
    for x in q_results:
        list_of_children = serialize_comments.deserialize_list(x[0])
        # print(list_of_children)
        big_string = get_all_text_from_children_comments(list_of_children)
    process_big_text(big_string)
