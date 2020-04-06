import numpy as np

def sigmoid(x):
    # np.exp(large number) will cause a warning of overflow
    return 2.0 / (1.0 + np.exp(-x)) - 1.0

def neg_abs(x):
    return -np.abs(x)

def neg_square(x):
    return -np.square(x)


def sqrt_abs(x):
    return np.sqrt(np.abs(x))

def neg_sqrt_abs(x):
    return -sqrt_abs(x)
