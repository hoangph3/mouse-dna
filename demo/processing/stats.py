import numpy as np


def __mean(x):
    if not len(x):
        return 0
    return float(np.mean(x))


def __std(x):
    if not len(x):
        return 0
    return float(np.std(x))


def __max(x):
    if not len(x):
        return 0
    return max(x)


def __min(x):
    if not len(x):
        return 0
    return min(x)