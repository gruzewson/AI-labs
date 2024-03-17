from itertools import compress
import random
import time
import matplotlib.pyplot as plt
import numpy
import copy


from data import *

def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]

def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))

def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness


items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200
n_selection = 20
n_elite = 1
genom_div = len(items) // 2 #'//' integer div

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)
probability = [population_size]

for _ in range(generations):
    population_history.append(copy.deepcopy(population))

    # TODO: implement genetic algorithm
    # choosing parents
    probability_sum = sum(fitness(items, knapsack_max_capacity, individual) for individual in population)
    probability = [fitness(items, knapsack_max_capacity, individual) / probability_sum for individual in population]

    parents = []
    for _ in range(n_selection):
        new_parent = population[numpy.random.choice(population_size, p=probability)]
        parents.append(new_parent)

    # creating new generation
    children = []
    for i in range(0, n_selection, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        child1 = parent1[:genom_div] + parent2[genom_div:]
        child2 = parent2[:genom_div] + parent1[genom_div:]
        children.append(child1)
        children.append(child2)

    #actualization
    new_population = []

    def fitness_key_function(individual):
        return fitness(items, knapsack_max_capacity, individual)

    sorted_population = sorted(population, key=fitness_key_function, reverse=False)
    new_population.extend(children)
    new_population.extend(sorted_population[len(children):])
    population = new_population

    # mutation
    for individual in population:
        index = random.randint(0, len(individual) - 1)
        if individual[index] == True:
            individual[index] = False
        else:
            individual[index] = True

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
