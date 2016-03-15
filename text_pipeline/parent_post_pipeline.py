# JEET's Parent Post Module Pipeline to get post info from Reddit API
import time

import praw

from text_pipeline import comment_db_manager

# User Agent String for Python API
user_agent = "PyAI UCI-CS175 1.5"


def get_list_of_ids_from_csv():
    """
    Function that gets saved ids of parent posts to get and returns them as a list
    :return: List(Tuples(String parent_post_id, String subreddit))
    """
    import csv
    list_of_post_tuples = []
    with open('/Users/jnagda/PycharmProjects/how-to-win-at-reddit/resources/google_query_ids/joce_2.csv',
              'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for row in csvreader:
            list_of_post_tuples.append((row[0], row[1]))
    return list_of_post_tuples


def truncate_identifier_from_id(id):
    return id[3:]


def get_parentpost_dict(r, parentPost):
    """
    Function that gets the dictionary of relevant information from Reddit API
    :param r: PRAW Agent
    :param parentPost: tuple(String parent_post_id, String subreddit)
    :return: Dictionary{Author,Id,URL,TimeCreated (utc), subreddit, subreddit_ID, Title, Score, Text}
    """
    link_id = truncate_identifier_from_id(parentPost[0])
    url_string = 'https://www.reddit.com/r/' + parentPost[1] + '/comments/' + link_id + '/.json'
    # example string
    # https://www.reddit.com/r/AskReddit/comments/37y5rx/what_do_you_always_say_yes_to/.json
    # print(url_string) #DEBUG PRINT STATEMENT
    try:
        t = r.get_submission(url_string)
        parent_info = vars(t)
        parentDict = {
            'author': '[deleted]' if parent_info['author'] is None else parent_info['author'].name,
            'id': parentPost[0],
            'url': parent_info['url'],
            'timecreated': parent_info['created_utc'],
            'subreddit_id': parent_info['subreddit_id'],
            'subreddit': parent_info['subreddit'].display_name,
            'title': parent_info['title'],
            'score': parent_info['score'],
            'selftext': '[deleted]' if parent_info['selftext'] is None else parent_info['selftext']
        }
        return parentDict
    except:
        return


def process_parent_data_pipeline():
    """
    Main process method that gets a list of ids to process and gets the dictionary of information from reddit
    NOTE: Post will only be inserted to DB if posted in May 2015
    Then attempts to insert this list into MySQL Database
    :return: None
    """
    r = praw.Reddit(user_agent=user_agent)
    start_time = time.time()
    x = 0  # iter counter
    list_of_dicts = []
    list_of_ids = get_list_of_ids_from_csv()
    print("got-ids")
    for parent_id in list_of_ids:
        print("GETTING:", x, parent_id)
        temp = get_parentpost_dict(r, parent_id)
        if temp is not None:
            time_created = temp['timecreated']
            if 1430438400.0 < time_created < 1433116799.0:
                list_of_dicts.append(temp)
        x += 1
    import json
    with open('backup_jeet_10000.json', 'w') as outfile:
        json.dump(list_of_dicts, outfile)
    from text_pipeline import mysql_manager
    mysql_manager.insert_parentdetails_BIG(list_of_dicts)
    print("--- %s seconds ---" % (time.time() - start_time))
    comment_db_manager.close_db_connection()
    mysql_manager.close_connection()


if __name__ == "__main__":
    # test= ('t3_2xedq9','SVExchange')
    # x = get_parentpost_dict(test)
    # print(x)
    process_parent_data_pipeline()
