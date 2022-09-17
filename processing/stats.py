import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Statistical functions
# [start, stop)
def __mean(array):
    start = 0
    stop = len(array)
    avg = 0
    counter = 0
    for i in range(start, stop):
        avg += array[i]
        counter += 1
    if counter == 0:
        return 0
    return avg / counter

# [start, stop)
def __std(array):
    start = 0
    stop = len(array)
    m = __mean(array)
    n = stop - start
    if n-1 <= 0:
        return 0
    s = 0

    for i in range(start+1, stop):
        s += (array[ i ]-m)*(array[i]-m)
    return math.sqrt(s/(n-1))

# [start, stop)
def __max(array):
    start = 0
    stop = len(array)
    n = stop - start
    if n-1 <= 0:
        return 0
    maxValue = array[start]
    for i in range(start, stop):
        if array[i] > maxValue:
            maxValue = array[ i ]
    return maxValue

# [start, stop)
def __min(array):
    start = 0
    stop = len(array)
    n = stop - start
    if n-1 <= 0:
        return 0
    minValue = array[stop-1]
    for i in range(start, stop):
        if array[i] != 0 and array[i] < minValue:
            minValue = array[ i ]
    return minValue
