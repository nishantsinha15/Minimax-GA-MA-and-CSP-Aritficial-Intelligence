import time
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

# M courses, N Halls, P professors
M = 30
N = 80
P = 20

threshhold = 0

# <course,professors,hall>
def fitness_function(chromosome):
    score = 0

    # One course should be taught by exactly one prof
    course = [[] for i in range(M)]
    count = [0 for i in range(M)]
    for i in chromosome:
        if i[1] not in course[i[0]]:
            course[i[0]].append(i[1])
            count[i[0]] += 1
    for i in count:
        score -= abs(i - 1)

    # One professor teaches max 2 slots in a day
    x = 0
    count = [0 for i in range(P)]
    for i in chromosome:
        if x % 8:
            count = [0 for i in range(P)]
            for j in count:
                score -= max(0, j - 2)
        count[i[1]] += 1
        x += 1
    for j in count:
        score -= max(0, j - 1)

    # One Professor teaches at max two courses
    count = [0 for i in range(P)]
    course = [[] for i in range(P)]
    for i in chromosome:
        if i[0] not in course[i[1]]:
            course[i[1]].append(i[0])
            count[i[1]] += 1
    for i in count:
        score -= min(abs(i - 2), abs(i - 1))

    return score > -1* threshhold


def stupid_init():
    chromosome = []
    for i in range(40):
        p = np.random.randint(0, P)
        c = np.random.randint(0, M)
        h = np.random.randint(0, N)
        chromosome.append((c, p, h))
    return chromosome


def backtrack(len, solution):
    if len >= 40:
        print("Solution found")
        print(solution)
        exit()
    c = np.random.permutation(M)
    p = np.random.permutation(P)
    h = np.random.permutation(N)

    for i in c:
        for j in p:
            for k in h:
                ok = True
                temp = solution + [(i,j,k)]
                if fitness_function(temp):
                    backtrack(len+1, temp)
    return False

def csp():
    global threshhold
    for i in range(100000):
        threshhold = i
        print("Running for threshhold of ",threshhold)
        backtrack(0, [])
        print("Failed to find a solution")


csp()