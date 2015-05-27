from pprint import pprint
import numpy as np
from tests import *
from utils import random_distribution, get_rounded, HIDDEN_NODES, OBSERVED_VALUES, EPS, generate_sample
from utils import random_distribution_list, get_probability, direction_match

# A_UNIFORM = [[1. / HIDDEN_NODES for _ in range(HIDDEN_NODES)] for _ in range(HIDDEN_NODES)]
# B_UNIFORM = [[1. / OBSERVED_VALUES for _ in range(OBSERVED_VALUES)] for _ in range(HIDDEN_NODES)]
# PI_UNIFORM = [1. / HIDDEN_NODES for _ in range(HIDDEN_NODES)]


def calcAlpha(seq, A, B, PI):
    T = len(seq)
    alpha = [[0.0 for _ in range(T)] for _ in range(HIDDEN_NODES)]
    for i in range(HIDDEN_NODES):
        alpha[i][0] = PI[i] * B[i][seq[0] - 1]
    for t in range(1, T):
        for j in range(HIDDEN_NODES):
            for i in range(HIDDEN_NODES):
                alpha[j][t] += B[j][seq[t] - 1] * alpha[i][t - 1] * A[i][j]
    return alpha


def calcBeta(seq, A, B):
    T = len(seq)
    beta = [[0.0 for _ in range(T)] for _ in range(HIDDEN_NODES)]
    for i in range(HIDDEN_NODES):
        beta[i][T - 1] = 1.0
    for t in range(T - 2, -1, -1):
        for i in range(HIDDEN_NODES):
            for j in range(HIDDEN_NODES):
                beta[i][t] += beta[j][t + 1] * A[i][j] * B[j][seq[t + 1] - 1]
    return beta


def calcGamma(alpha, beta, T):
    gamma = [[0.0 for _ in range(T)] for _ in range(HIDDEN_NODES)]
    for t in range(T):
        den = 0.0
        for j in range(HIDDEN_NODES):
            den += alpha[j][t] * beta[j][t]
        for i in range(HIDDEN_NODES):
            gamma[i][t] = alpha[i][t] * beta[i][t] / den
    return gamma


def calcKsi(seq, A, B, alpha, beta):
    T = len(seq)
    ksi = [[[0.0 for _ in range(T - 1)] for _ in range(HIDDEN_NODES)] for _ in range(HIDDEN_NODES)]
    for t in range(T - 1):
        den = 0.0
        for k in range(HIDDEN_NODES):
            den += alpha[k][t] * beta[k][t]

        for i in range(HIDDEN_NODES):
            for j in range(HIDDEN_NODES):
                ksi[i][j][t] = alpha[i][t] * A[i][j] * beta[j][t + 1] * B[j][seq[t + 1] - 1] / den
    return ksi


def calcPI(gamma):
    PI = [0.0 for _ in range(HIDDEN_NODES)]
    for i in range(HIDDEN_NODES):
        PI[i] = gamma[i][0]
    return PI


def calcA(ksi, gamma, T):
    A = [[0.0 for _ in range(HIDDEN_NODES)] for _ in range(HIDDEN_NODES)]
    for i in range(HIDDEN_NODES):
        den = 0.0
        for t in range(T - 1):
            den += gamma[i][t]
        for j in range(HIDDEN_NODES):
            num = 0.0
            for t in range(T - 1):
                num += ksi[i][j][t]
            A[i][j] = num / den
    return A


def calcB(seq, gamma):
    T = len(seq)
    B = [[0.0 for _ in range(OBSERVED_VALUES)] for _ in range(HIDDEN_NODES)]
    for i in range(HIDDEN_NODES):
        den = 0.0
        for t in range(T):
            den += gamma[i][t]
        for v in range(OBSERVED_VALUES):
            num = 0.0
            for t in range(T):
                if seq[t] - 1 == v:
                    num += gamma[i][t]
            B[i][v] = num / den
    return B


def twoDimDifMax(m1, m2):
    maximum = 0.
    for i in range(len(m1)):
        maximum = max(maximum, oneDimDifMax(m1[i], m2[i]))
    return maximum


def oneDimDifMax(m1, m2):
    maximum = 0.
    for i in range(len(m1)):
        maximum = max(maximum, abs(m1[i] - m2[i]))
    return maximum


def baum_welch(seq, A, B, PI):
    while True:
        alpha = calcAlpha(seq, A, B, PI)
        beta = calcBeta(seq, A, B)
        gamma = calcGamma(alpha, beta, len(seq))
        ksi = calcKsi(seq, A, B, alpha, beta)
        PI_STAR = calcPI(gamma)
        A_STAR = calcA(ksi, gamma, len(seq))
        B_STAR = calcB(seq, gamma)
        if twoDimDifMax(A, A_STAR) < EPS and oneDimDifMax(B[1], B_STAR[1]) < EPS and oneDimDifMax(PI, PI_STAR) < EPS:
            return A, B, PI
        A = A_STAR
        B[1] = B_STAR[1]
        PI = PI_STAR
    return None


def get_initials():
    A = random_distribution_list(HIDDEN_NODES, HIDDEN_NODES)
    B = [[1/6. for _ in range(6)], random_distribution(6)]
    PI = random_distribution(HIDDEN_NODES)
    return A, B, PI


def run_on_seq(seq):
    A, B, PI = get_initials()
    return baum_welch(seq, A, B, PI)


def run_on_test_data(data, size=10):
    observations, _ = generate_sample(data, size=size)
    return run_on_seq(observations), observations


def main():
    test = Test1()
    a, b, pi = run_on_test_data(test, size=100)
    pprint(get_rounded(a))
    pprint(get_rounded(b))
    pprint(get_rounded(pi))
    test_data_dif = CasinoTestData()
    #print(dict_to_matrix(test.transition_probability))
    #print(a)
    a_dif = np.subtract(dict_to_matrix(test.transition_probability), a)
    b_dif = np.subtract(dict_to_matrix(test.emission_probability), b)
    pi_dif = np.subtract(test.start_probability.values(), pi)
    print(calculate_std(dict_to_matrix(test.transition_probability), dict_to_matrix(test.emission_probability), test.start_probability.values()))
    print(calculate_std(a_dif, b_dif, pi_dif))

def perform_tests(test_count, size=100):
    test_results_a = 0
    test_results_pi = 0

    #prob = 0.0
    #prob_res = 0.0
    test_b_sum = 0.0
    test_b_mean = 0.0
    for i in xrange(test_count):
        a, b, pi = get_initials()
        (a_res, b_res, pi_res), observations = run_on_test_data(convert_to_test_data(a, b, pi), size=size)

        a_dif = np.subtract(a_res, a)
        b_dif = np.subtract(b_res, b)
        pi_dif = np.subtract(pi_res, pi)

        b_dif = np.subtract(b[1], b_res[1])
        b_dif = map(abs, b_dif)
        test_b_sum += sum(b_dif)
        test_b_mean += np.array(b_dif).mean()


        for i in range(len(a)):
            test_results_a += direction_match(a[i], a_res[i])

        test_results_pi += direction_match(pi, pi_res)

        #prob += get_probability(a,b,pi, observations)
        #prob_res += get_probability(a_res, b_res,pi_res, observations)

        #print(a)
        #print(a_res)
        #print(b)
        #print(b_res)
        #print(pi)
        #print(pi_res)

    print(float(test_results_a) / 2 / test_count)
    print
    print(test_b_sum / test_count)
    print(test_b_mean / test_count)
    print
    print(float(test_results_pi) / test_count)

perform_tests(1000, size=100)