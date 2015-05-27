from pprint import pformat
from utils import DICE_1, DICE_2, random_distribution, get_rounded


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


def generate_random_test_data():
    start = random_distribution(2)
    d1_to_d2 = random_distribution(2)
    d2_to_d1 = random_distribution(2)
    dice_1 = random_distribution(6)
    dice_2 = random_distribution(6)

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


def calculate_std(test_data):
    # TODO please implement
    pass