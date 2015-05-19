from scipy import stats
import numpy as np


DICE_1 = 0
DICE_2 = 1
STATES = (DICE_1, DICE_2)


def viterbi(observations, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for state in STATES:
        V[0][state] = start_p[state] * emit_p[state][observations[0]]
        path[state] = [state]

    # Run Viterbi for t > 0
    for t in xrange(1, len(observations)):
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


def build_distribution(dist, name=None):
    return stats.rv_discrete(values=(np.array(dist.keys()), np.array(dist.values())),
                             name=name)


def generate_sample(dice_1, dice_2, trans_p, start_p, size=50):
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


def perform_tests(test_count, size=100):
    start_probability = {DICE_1: 0.9, DICE_2: 0.1}
    transition_probability = {
        DICE_1: {DICE_1: 0.95, DICE_2: 0.05},
        DICE_2: {DICE_1: 0.5, DICE_2: 0.5},
    }
    emission_probability = {
        DICE_1: {x: 1/6. for x in range(1, 7)},
        DICE_2: {1: 1/10., 2: 1/10., 3: 1/10., 4: 1/10., 5: 1/10., 6: 5/10.}
    }
    test_results = []
    for i in xrange(test_count):
        observations, result_states = generate_sample(emission_probability[DICE_1],
                                                      emission_probability[DICE_2],
                                                      transition_probability, start_probability,
                                                      size=size)
        prob, path = viterbi(observations,
                             start_probability,
                             transition_probability,
                             emission_probability)

        hamming = [0 if a == b else 1 for a, b in zip(path, result_states)]
        test_results.append(sum(hamming))
        # print ''.join(map(str, path))
        # print ''.join(map(str, result_states))
        # result_mask = ''.join(map(str, hamming))
        # print result_mask
    np_res = np.array(test_results)
    print np_res.mean()


perform_tests(1000, size=50)