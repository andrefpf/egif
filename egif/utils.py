import numpy as np

def sigmoid(x):
    return 1 / (1 + 2**x)

def is_pow_2(x):
    # it is a bit manipulation hack 
    # if x = 8 = 1000
    # then x-1 = 7 = 0111
    # then 1000 and 0111 = 0
    return (x != 0) and (x & (x-1) == 0)