import numpy as np
import matplotlib.pyplot as  plt
import mysql_manager

def histogram_document_length():
    '''
    Create an array of document lengths and plot them.
    [only including parentPost for now] 2/21/16
    :return:
    '''
    conn = mysql_manager.cnx
    c =  conn.cursor()
    c.execute("SELECT selftext FROM ParentPostDetails")

    x = []
    for text in c.fetchall():
        text = text[0]
        x.append(len(text))

    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
    plt.show()

if __name__ == '__main__':
    histogram_document_length()