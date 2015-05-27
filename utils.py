import random
from scipy import stats
import numpy as np


DICE_1 = 0
DICE_2 = 1
STATES = (DICE_1, DICE_2)
HIDDEN_NODES = 2
OBSERVED_VALUES = 6
EPS = 0.001


def get_rounded(matrix, precision=3):
    """
    Use it for printing only!
    """
    if not isinstance(matrix, (list, tuple)):
        return matrix
    result = []
    if isinstance(matrix[0], (list, tuple)):
        for l in matrix:
            result.append(get_rounded(l))
    else:
        for x in matrix:
            result.append(round(x, ndigits=precision))
    return result


def random_distribution_list(list_size, distr_size):
    result = []
    for i in range(list_size):
        result += [random_distribution(distr_size)]
    return result


def random_distribution(length):
    lst = []
    for j in range(length - 1):
        lst += [random.uniform(0., 1. - sum(lst))]
    lst += [1 - sum(lst)]
    return lst

def get_probability(a, b, pi, observations):
    probabilities = []
    for i in range(len(pi)):
        probabilities.append((i, pi[i]))
    for j in range(len(observations)):
        c = observations[j]
        new_probabilities = []
        for n, prob in probabilities:
            for i in range(len(a)):
                new_probabilities.append((i, prob * b[n][c - 1] * (1.0 if (j == len(observations) - 1) else a[n][i])))
        probabilities = new_probabilities
    res = 0.0
    for _, prob in probabilities:
        res += prob
    return res


def build_distribution(dist, name=None):
    return stats.rv_discrete(values=(np.array(dist.keys()), np.array(dist.values())),
                             name=name)


def generate_sample(data, size=50):
    """
    :type data: CasinoTestData
    """
    dice_1 = data.emission_probability[DICE_1]
    dice_2 = data.emission_probability[DICE_2]
    trans_p = data.transition_probability
    start_p = data.start_probability
    d1 = build_distribution(dice_1, str(DICE_1))
    d2 = build_distribution(dice_2, str(DICE_2))
    d1_to_d2 = build_distribution(trans_p[DICE_1])
    d2_to_d1 = build_distribution(trans_p[DICE_2])
    start_dist = build_distribution(start_p)
    # current == 0 -> DICE_1
    # current == 1 -> DICE_2
    distributions, current = [d1, d2], 0 if start_dist.rvs() == DICE_1 else 1
    obs, states = [], []
    for i in range(size):
        d = distributions[current]
        obs.append(d.rvs())
        states.append(current)
        # if d is DICE_1 distribution and we need swap
        if current == 0 and d1_to_d2.rvs() == DICE_2:
            current = 1 - current
        # if d is DICE_2 distribution and we need swap
        elif current == 1 and d2_to_d1.rvs() == DICE_1:
            current = 1 - current
    return obs, states