import random
from tests import Test1
from utils import random_distribution, print_rounded, HIDDEN_NODES, OBSERVED_VALUES, EPS, generate_sample
from utils import random_distribution_list

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
    max = 0.0
    for i in range(len(m1)):
        for j in range(len(m1[i])):
            val = abs(m1[i][j] - m2[i][j])
            if max < val:
                max = val
    return max


def oneDimDifMax(m1, m2):
    max = 0.0
    for i in range(len(m1)):
        val = abs(m1[i] - m2[i])
        if max < val:
            max = val
    return max


def baum_welch(seq, A, B, PI):
    while True:
        alpha = calcAlpha(seq, A, B, PI)
        beta = calcBeta(seq, A, B)
        gamma = calcGamma(alpha, beta, len(seq))
        ksi = calcKsi(seq, A, B, alpha, beta)
        PI_STAR = calcPI(gamma)
        A_STAR = calcA(ksi, gamma, len(seq))
        B_STAR = calcB(seq, gamma)
        if twoDimDifMax(A, A_STAR) < EPS and twoDimDifMax(B, B_STAR) < EPS and oneDimDifMax(PI, PI_STAR) < EPS:
            return A, B, PI
        A = A_STAR
        B = B_STAR
        PI = PI_STAR
    return None


def get_initials():
    A = random_distribution_list(HIDDEN_NODES, HIDDEN_NODES)
    B = random_distribution_list(HIDDEN_NODES, OBSERVED_VALUES)
    PI = random_distribution(HIDDEN_NODES)
    return A, B, PI


def run_on_seq(seq):
    A, B, PI = get_initials()
    return baum_welch(seq, A, B, PI)


def run_on_test_data(data, size=10):
    observations, _ = generate_sample(data, size=size)
    return run_on_seq(observations)


def main():
    # random_seq = [random.randint(1, OBSERVED_VALUES) for _ in range(10)]
    # A_RES, B_RES, PI_RES = run_on_seq(random_seq)
    # print_rounded(A_RES)
    # print_rounded(B_RES)
    # print_rounded(PI_RES)

    test = Test1()
    a, b, pi = run_on_test_data(test)
    print_rounded(a)
    print_rounded(b)
    print_rounded(pi)


main()