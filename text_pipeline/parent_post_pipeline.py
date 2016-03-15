# JEET's Parent Post Module Pipeline
import time
import praw
from text_pipeline import comment_db_manager


def get_list_of_ids_from_csv():
    import csv
    list_of_post_tuples = []
    with open('/Users/jnagda/PycharmProjects/how-to-win-at-reddit/resources/jeet_25000.csv',
              'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for row in csvreader:
            list_of_post_tuples.append((row[0], row[1]))
    return list_of_post_tuples


def truncate_identifier_from_id(id):
    return id[3:]


def get_parentpost_dict(parentPost):
    user_agent = "PyAI UCI-CS175 1.5"
    link_id = truncate_identifier_from_id(parentPost[0])
    url_string = 'https://www.reddit.com/r/' + parentPost[1] + '/comments/' + link_id + '/.json'
    # example string
    # https://www.reddit.com/r/AskReddit/comments/37y5rx/what_do_you_always_say_yes_to/.json
    # print(url_string) #DEBUG PRINT STATEMENT
    r = praw.Reddit(user_agent=user_agent)
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
    start_time = time.time()
    x = 0
    list_of_dicts = []
    list_of_ids = get_list_of_ids_from_csv()
    print("got-ids")
    for parent_id in list_of_ids:
        print("GETTING:", x, parent_id)
        temp = get_parentpost_dict(parent_id)
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
