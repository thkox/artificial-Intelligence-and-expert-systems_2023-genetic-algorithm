import random
import networkx as nx
from matplotlib import pyplot as plt

graph = {
    1: [2, 3, 4, 13, 15, 16],
    2: [1, 3, 5, 8, 9, 14, 15, 16],
    3: [1, 2, 4, 5, 6],
    4: [1, 3, 6, 13],
    5: [2, 3, 6, 7, 9, 10],
    6: [3, 4, 5, 7, 11, 13],
    7: [5, 6, 10, 11],
    8: [2, 9, 14],
    9: [2, 5, 8, 10, 12, 14],
    10: [5, 7, 9, 11, 12],
    11: [6, 7, 10, 12, 13],
    12: [9, 10, 11, 13, 14, 15],
    13: [1, 4, 6, 11, 12, 15],
    14: [2, 8, 9, 12, 15],
    15: [1, 2, 12, 13, 14, 16],
    16: [1, 2, 15]
}
colors = ["Red", "Green", "Blue", "Yellow"]


def create_population():
    population_list = []
    for k in range(population_size):
        individual_dict = {node: random.choice(colors) for node in graph.keys()}
        population_list.append(individual_dict)
    print("Population created successfully!")
    return population_list


def fitness(individual_dict):
    fitness_counter = 0
    for node in graph:
        for neighbor in graph[node]:
            if individual_dict[node] != individual_dict[neighbor]:
                fitness_counter += 1
    print("Fitness score for an individual is:", int(fitness_counter / 2))
    return int(fitness_counter / 2)  # Because we are counting each edge twice


def fitness_score_per_individual(population_list):
    fitness_scores = {}
    for k, individual_dict in enumerate(population_list):
        fitness_scores[k] = fitness(individual_dict)
    return fitness_scores


# We are going to select the parents using roulette wheel selection
def select_parents(population_list, fitness_scores):
    # Calculate the sum of all fitness scores
    sum_of_fitness_scores = sum(fitness_scores)
    # Calculate the probability of each individual
    probabilities = [fitness_score_count / sum_of_fitness_scores for fitness_score_count in
                     fitness_scores]  # fitness_score / sum_of_fitness_scores = probability
    # Calculate the cumulative probability of each individual
    cumulative_probabilities = [sum(probabilities[:k + 1]) for k in range(len(probabilities))]
    # Select two parents
    parents_list = []
    for k in range(2):
        random_number = random.random()
        for (index, individual_dict) in enumerate(population_list):
            if random_number <= cumulative_probabilities[index]:
                parents_list.append(individual_dict)
                break
    if len(parents_list) != 2:
        print("Error in selecting parents")
    return parents_list


def crossover(parent1, parent2):
    crossover_point = random.randint(1, num_of_nodes - 1)  # We don't want to include the last node
    child1 = {}
    child2 = {}
    for k, node in enumerate(graph.keys()):
        if k <= crossover_point:
            child1[node] = parent1[node]
            child2[node] = parent2[node]
        else:
            child1[node] = parent2[node]
            child2[node] = parent1[node]
    return child1, child2


def mutation(child1, child2):
    child = random.choice([child1, child2])
    for node in graph:
        for neighbor in graph[node]:
            if child[node] == child[neighbor]:
                colors_temp = colors.copy()
                colors_temp.remove(child[node])
                child[node] = random.choice(colors_temp)  # We don't want to have the same color as the neighbor
                break
    return child1, child2


def create_children(parent1, parent2):
    child1 = {}
    child2 = {}
    random_number = random.randint(0, 2)
    if random_number == 0:
        child1, child2 = crossover(parent1, parent2)
    elif random_number == 1:
        child1, child2 = mutation(parent1, parent2)
    elif random_number == 2:
        child1, child2 = crossover(parent1, parent2)
        child1, child2 = mutation(child1, child2)
    return child1, child2


if __name__ == '__main__':
    print("Genetic Algorithm for coloring graph")
    print("Created by: Theodoros Koxanoglou, ΑΜ: P20094")
    parents = []
    mates = []
    children = []
    num_of_nodes = len(graph)
    print("The number of nodes in the graph is:", num_of_nodes)
    population_size = 100
    print("We manually set the population size to", population_size, "individuals")
    # Create population
    population = create_population()
    # Calculate fitness
    fitness_scores_dict = fitness_score_per_individual(population)

    correct_fitness_score = 42
    for i in range(100):
        print("------------------------------Generation:", i + 1, "------------------------------")
        # Select parents
        for j in range(len(population) // 2):
            mates.append(select_parents(population, fitness_scores_dict))
        # Create children
        for j in range(len(mates)):
            children.extend(
                create_children(mates[j][0], mates[j][1]))  # We need to create two children for each pair of parents

        population = children  # We need to replace the old population with the new one
        children = []
        mates = []
        parents = []

        # Calculate fitness
        fitness_scores_dict = fitness_score_per_individual(population)
        if correct_fitness_score in fitness_scores_dict.values():
            print("We found a solution!")
            break
    sorted_fitness_scores_dict = dict(sorted(fitness_scores_dict.items(), key=lambda x: x[1]))
    solution = list(sorted_fitness_scores_dict.keys())[-1]
    if fitness_scores_dict[solution] == correct_fitness_score:
        print("The solution is:", population[solution])
    else:
        print("The optimal solution is:", population[solution], "with fitness score:", solution,
              "and percentage:", "{:.2f}%".format(solution / correct_fitness_score * 100))
    G = nx.Graph()
    G.add_nodes_from(graph.keys())
    for node in graph:
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)
    nx.draw(G, with_labels=True, font_weight='bold', node_color=list(population[solution].values()))
    plt.show()
    print("Thank you for using the Genetic Algorithm for coloring graph")
