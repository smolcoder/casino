from utils import DICE_1, DICE_2


class CasinoTestData:
    start_probability = None
    transition_probability = None
    emission_probability = None


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
        DICE_2: {DICE_1: 0.6, DICE_2: 0.4},
        }
    emission_probability = {
        DICE_1: {x: 1/6. for x in range(1, 7)},
        DICE_2: {1: 1/10., 2: 1/10., 3: 1/10., 4: 1/10., 5: 1/10., 6: 5/10.}
    }


def generate_random_test_data():
    # TODO please implement
    pass


def calculate_std(test_data):
    # TODO please implement
    pass