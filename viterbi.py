import numpy as np
from generator import STATES, DICE_1, DICE_2, generate_sample


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


def perform_tests(test_count, size=100):
    start_probability = {DICE_1: 0.9, DICE_2: 0.1}
    transition_probability = {
        DICE_1: {DICE_1: 0.95, DICE_2: 0.05},
        DICE_2: {DICE_1: 0.30, DICE_2: 0.70},
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


perform_tests(500, size=50)