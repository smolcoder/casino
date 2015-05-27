import numpy as np
from pprint import pprint
from utils import STATES, generate_sample
from tests import generate_random_test_data
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt


def viterbi(observations, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for state in STATES:
        V[0][state] = start_p[state] * emit_p[state][observations[0]]
        path[state] = [state]

    # Run Viterbi for t > 0
    for t in range(1, len(observations)):
        V.append({})
        new_path = {}

        for cur in STATES:
            prob, previous = max((V[t - 1][prev] * trans_p[prev][cur] * emit_p[cur][observations[t]], prev)
                                 for prev in STATES)
            V[t][cur] = prob
            new_path[cur] = path[previous] + [cur]

        path = new_path
    n = len(observations) - 1
    prob, state = max((V[n][y], y) for y in STATES)
    return prob, path[state]


def get_mean_hamming(data, test_count=20, size=20):
    test_results = []
    for i in xrange(test_count):
        observations, result_states = generate_sample(data, size=size)
        prob, path = viterbi(observations,
                             data.start_probability,
                             data.transition_probability,
                             data.emission_probability)

        hamming = [0 if a == b else 1 for a, b in zip(path, result_states)]
        test_results.append(sum(hamming))
        # print ''.join(map(str, path))
        # print ''.join(map(str, result_states))
        # print ''.join(map(str, hamming))
    np_res = np.array(test_results)
    return np_res.mean()


def count_statistics():
    means = []
    for _ in range(100):
        data = generate_random_test_data()
        means.append(get_mean_hamming(data))
    means = np.array(means)
    return means.mean(), means.std()


print count_statistics()