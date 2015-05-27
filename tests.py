from pprint import pformat
from utils import DICE_1, DICE_2, random_distribution, get_rounded, random_almost_uniform_distribution
from math import sqrt


class CasinoTestData:
    start_probability = None
    transition_probability = None
    emission_probability = None

    def __str__(self):
        res = 'Start probability distribution:\n{}\n'.format(pformat(get_rounded(self.start_probability.values())))
        res += 'Transition probability distribution:\n{}\n'.format(pformat(
            [get_rounded(self.transition_probability[DICE_1].values()),
             get_rounded(self.transition_probability[DICE_2].values())]))
        res += 'Emission probability distribution:\n{}'.format(pformat(get_rounded(
            [get_rounded(self.emission_probability[DICE_1].values()),
             get_rounded(self.emission_probability[DICE_2].values())]
        )))
        return res


class Test2(CasinoTestData):
    start_probability = {DICE_1: 0.9, DICE_2: 0.1}
    transition_probability = {
        DICE_1: {DICE_1: 0.95, DICE_2: 0.05},
        DICE_2: {DICE_1: 0.30, DICE_2: 0.70},
        }
    emission_probability = {
        DICE_1: {x: 1/6. for x in range(1, 7)},
        DICE_2: {1: 1/10., 2: 1/10., 3: 1/10., 4: 1/10., 5: 1/10., 6: 5/10.}
    }


class Test1(CasinoTestData):
    start_probability = {DICE_1: 0.9, DICE_2: 0.1}
    transition_probability = {
        DICE_1: {DICE_1: 0.8, DICE_2: 0.2},
        DICE_2: {DICE_1: 0.3, DICE_2: 0.7},
        }
    emission_probability = {
        DICE_1: {x: 1/6. for x in range(1, 7)},
        DICE_2: {1: 1/10., 2: 1/10., 3: 1/10., 4: 1/10., 5: 1/10., 6: 5/10.}
    }


def generate_random_test_data(with_fair=True, almost_uniform=False):
    start = random_distribution(2)
    d1_to_d2 = random_distribution(2)
    d2_to_d1 = random_distribution(2)
    dice_1 = [1/6. for _ in range(6)] if with_fair else random_distribution(6)
    dice_2 = random_almost_uniform_distribution() if almost_uniform else random_distribution(6)

    res = CasinoTestData()
    res.start_probability = {DICE_1: start[0], DICE_2: start[1]}
    res.transition_probability = {
        DICE_1: {DICE_1: d1_to_d2[0], DICE_2: d1_to_d2[1]},
        DICE_2: {DICE_1: d2_to_d1[0], DICE_2: d2_to_d1[1]},
    }
    res.emission_probability = {
        DICE_1: {x: prob for x, prob in zip([1, 2, 3, 4, 5, 6], dice_1)},
        DICE_2: {x: prob for x, prob in zip([1, 2, 3, 4, 5, 6], dice_2)},
    }
    return res

def convert_to_test_data(a, b, pi):
    res = CasinoTestData()
    res.start_probability = list_to_dict(pi)
    res.transition_probability = matrix_to_dict(a, list_to_dict)
    res.emission_probability = matrix_to_dict(b, em_prob_to_dict)
    return res

def list_to_dict(l):
        return {i: l[i] for i in range(len(l))}

def em_prob_to_dict(l):
    return {i + 1: l[i] for i in range(len(l))}

def matrix_to_dict(matrix, f):
    return {i: f(matrix[i]) for i in range(len(matrix))}

def calculate_list_sts(l):
    return sqrt(sum([i ** 2 for i in l]) / len(l))

def calculate_matrix_std(matrix):
    return sqrt(sum([sum([i ** 2 for i in row]) for row in matrix]) / (len(matrix) * len(matrix[0])))

def dict_to_matrix(d):
    return [row.values() for row in d.values()]

def calculate_std(a, b, pi):
    return calculate_matrix_std(a), \
           calculate_matrix_std(b), \
           calculate_list_sts(pi)