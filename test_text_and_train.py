from text_pipeline import comment_db_manager
from text_pipeline import mysql_manager
from text_pipeline import serialize_comments

sql_statement = "SELECT parentPost_id,childrenComments,score,url,selftext FROM ParentPostDetails LIMIT 20"

sql_statement_children = "SELECT body,author FROM May2015 WHERE id = "


def get_all_text_from_children_comments(list_of_children):
    big_string = ""
    for child in list_of_children:
        test_string = sql_statement_children + "\'" + child + "\'"
        t = comment_db_manager.perform_query('/Users/jnagda/Documents/Reddit_Comments/database.sqlite', test_string)
        big_string = big_string + str(t[0][0]) + str(t[0][1])
    return big_string


def tokenize_simple(document):
    import re, string
    document = document.lower()  # convert document to lower case
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    document = regex.sub(' ', document)  # replace all punctuation marks with single spaces
    document = re.sub('\s+', ' ',
                      document).strip()  # replace one or more spaces with single space AND strip leading/trailng whitespace
    return document.split()  # return list of tokens splitting o    n single space


def remove_stopwords_inner(tokens, stopwords):
    stopwords = set(stopwords)
    return [x for x in tokens if x not in stopwords]


def remove_stopwords_nltk(tokens):
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


def decision_tree_pipeline(train_data, train_targets, test_data):
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import CountVectorizer
    from nltk.corpus import stopwords
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.tree import DecisionTreeClassifier
    text_clf_bernNB = Pipeline([('vect', CountVectorizer(stop_words=stopwords.words('english'))),
                                ('tfidf', TfidfTransformer()),
                                ('clf', DecisionTreeClassifier()),
                                ])
    text_clf_bernNB = text_clf_bernNB.fit(train_data, train_targets)
    predicted_bernNB = text_clf_bernNB.predict(test_data)
    return predicted_bernNB



if __name__ == '__main__':
    q_results = mysql_manager.perform_query(sql_statement)
    big_string = ""
    train_data = []
    train_targets = []
    test_data = []
    test_targets = []
    for (id, comments, score, url, selftext) in q_results[:10]:
        list_of_children = serialize_comments.deserialize_list(comments)
        # print(list_of_children)
        big_string = get_all_text_from_children_comments(list_of_children)
        if url is not None:
            big_string += url
        if selftext is not None:
            big_string += selftext
        train_data.append(big_string)
        if score > 100:
            train_targets.append(1)
        else:
            train_targets.append(0)
    for (id, comments, score, url, selftext) in q_results[10:]:
        list_of_children = serialize_comments.deserialize_list(comments)
        # print(list_of_children)
        big_string = get_all_text_from_children_comments(list_of_children)
        test_data.append(big_string)
        if score > 100:
            test_targets.append(1)
        else:
            test_targets.append(0)
    x = decision_tree_pipeline(train_data, train_targets, test_data)
