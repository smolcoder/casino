import numpy as np
from utils import STATES, generate_sample
from tests import Test1


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
    test_results = []
    test = Test1()
    for i in xrange(test_count):
        observations, result_states = generate_sample(test, size=size)
        prob, path = viterbi(observations,
                             test.start_probability,
                             test.transition_probability,
                             test.emission_probability)

        hamming = [0 if a == b else 1 for a, b in zip(path, result_states)]
        test_results.append(sum(hamming))
        # print ''.join(map(str, path))
        # print ''.join(map(str, result_states))
        # result_mask = ''.join(map(str, hamming))
        # print result_mask
    np_res = np.array(test_results)
    print np_res.mean()


perform_tests(1000, size=20)