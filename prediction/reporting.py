from operator import itemgetter

import numpy as np


def report(grid_scores, n_top=3):
    """
    Found this function on an example of Scikitlearn with RandomSearch!
    :param grid_scores: grid_scores object to evaluate
    :param n_top: number of top models to show
    :return: None
    """
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
            score.mean_validation_score,
            np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")
