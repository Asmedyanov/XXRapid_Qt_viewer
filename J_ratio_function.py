import numpy as np
from scipy.optimize import fsolve


def decrement_space_function(a, w, h):
    return np.sinh(a * w / 2) - a * h


# decrement_space_function_vect = np.vectorize(lambda a, w, h: decrement_space_function(a, w, h))


def decrement_space(w, h):
    return fsolve(decrement_space_function, x0=1 / w, args=(w, h))


def sinch(x):
    return np.where(x == 0, 0, np.sinh(x) / x)


def j_ratio(t, w, h, t_0):
    a = decrement_space(w, h)
    return np.power(sinch(a * w / 2), (t / t_0) - 1)
