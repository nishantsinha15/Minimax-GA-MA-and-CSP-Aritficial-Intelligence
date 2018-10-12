import time
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

# M courses, N Halls, P professors
M = 30
N = 80
P = 20


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
                score -= max( 0, j-2)
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

    return score


def init_population(count):
    population = []
    for i in range(count):
        chromosome = []
        p = np.random.permutation(P)
        c = np.random.permutation(M)
        h = np.random.permutation(N)
        while len(p) < 40:
            p = np.concatenate((p, p))
        while len(c) < 40:
            c = np.concatenate((c, c))
        while len(h) < 40:
            h = np.concatenate((h, h))

        for j in range(40):
            chromosome.append((c[j], p[j], h[j]))

        population.append(chromosome)
    return population


def stupid_init(count):
    population = []
    for i in range(count):
        chromosome = []
        for i in range(40):
            p = np.random.randint(0, P)
            c = np.random.randint(0, M)
            h = np.random.randint(0, N)
            chromosome.append((c,p,h))
        population.append(chromosome)
    return population


def selection(population, score):
    temp = []
    for i, j in zip(population, score):
        temp.append((j, i))
    temp.sort(reverse=True)
    ret = []
    for i in temp[:10]:
        ret.append(i[1])
    return ret


def compute_fitness(population):
    score = []
    for i in population:
        score.append(fitness_function(i))
    return score


# create 90 more samples from the 10 samples here
def crossover(population):
    for _ in range(45):
        i, j = np.random.randint(0, 10), np.random.randint(0, 10)
        point = np.random.randint(0, 40)
        temp1 = population[i][:point] + population[j][point:]
        temp2 = population[j][:point] + population[i][point:]
        population.append(temp1)
        population.append(temp2)
    return population[:100]


def Genetic_Algorithm():
    best = []
    worst = []
    average = []
    t1 = time.time()
    population = stupid_init(100)
    score = compute_fitness(population)
    prev = 0
    iter = 0
    while abs(mean(score) - prev) > 0:
        iter += 1
        best.append(-1*max(score))
        worst.append(-1*min(score))
        average.append(-1*mean(score))
        print("Iteration ", iter)
        prev = mean(score)
        population = selection(population, score)
        population = crossover(population)
        score = compute_fitness(population)
    t2 = time.time()
    print("Converged in ",t2-t1 ," seconds")
    plt.plot(best, 'g', worst, 'r', average, 'b')
    plt.savefig('Genetic Algorithm.png')
    # plt.show()


Genetic_Algorithm()

