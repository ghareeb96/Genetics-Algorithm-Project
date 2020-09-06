import random


# initialize the population with 100 chromosome
def initial_population():
    individuals = 100
    p = []

    for i in range(individuals):
        chromosome = []
        # [a,b,c,d,e,f,g,h,i,j]
        for number in range(10):
            chromosome.append(random.randint(0, 9))
        p.append(chromosome)
    return p


# calculating the fitness for any list of pop.
def calculate_fitness(p):
    # f(x) = (4 * a * c) – (8 * b * d) + (5 * h * i) − (10 * g * j) + (e * f)
    fitness_list = []
    for i in range(len(p)):
        fitness_function = (4*(p[i][0])*(p[i][2])) - (8*(p[i][1])*(p[i][3])) + (5*(p[i][7])*(p[i][8])) - (10*(p[i][6])*(p[i][9])) + ((p[i][4])*(p[i][5]))
        fitness_list.append(fitness_function)
    return fitness_list


# selecting by roulette wheel and handling the -ve values cases
def roulette_wheel_selection(f):
    roulette_probs = []
    new_fitness = []
    min_fit = abs(min(f))
    for i in range(len(f)):
        new_fitness.append(f[i] + min_fit + 1)
    fitness_sum = sum(new_fitness)
    prob_sum = 0
    for i in range(len(new_fitness)):
        prob_sum += new_fitness[i]
        roulette_probs.append((prob_sum/fitness_sum))
    rnd = random.random()
    for i in range(len(roulette_probs)):
        if rnd <= roulette_probs[i]:
            return i


# crossover between selected parents with prob 0.9
def crossover(parent1, parent2):
    offspring = []
    child1 = []
    child2 = []
    point1 = random.randint(0, 8)
    point2 = random.randint(point1 + 1, 9)
    child1.extend(parent1[0:point1])
    child2.extend(parent2[0:point1])
    while point1 <= point2:
        child1.append(parent2[point1])
        child2.append(parent1[point1])
        point1 += 1
    if point2 != 9:
        child1.extend(parent1[point2 + 1:10])
        child2.extend(parent2[point2 + 1:10])
    offspring.append(child1)
    offspring.append(child2)
    return offspring


# mutation of chromosome with prob 0.08
def mutation(chromosome):
    chromosome[6] = int(chromosome[6] / 2)
    return chromosome


# calculating the fittest of a fitness list
def best_fit(f):
    return f.index(max(f))


# Entering the Number of Generations
gen = int(input("Enter number of Generations : \n"))
crossover_probability = 0.9
mutation_probability = 0.08

initial_generation = initial_population()
initial_fitness = calculate_fitness(initial_generation)
best_fitness = best_fit(initial_fitness)

# Storing the initial values in a file
initial_file = open("initial generation.txt", "w")
initial_file.write("     Initial Generation            Fitness \n")
initial_file.write("===========================================\n")
for ind in range(len(initial_generation)):
    initial_file.write(str(initial_generation[ind]) + "      " + str(initial_fitness[ind]) + "\n")
initial_file.write("\nBest Fit in the Generation : " + "\n")
initial_file.write(str(initial_generation[best_fitness]) + "      " + str(initial_fitness[best_fitness]) + "\n")
initial_file.close()


fitness = initial_fitness
population = initial_generation
file2 = open("generations progress.txt", "w")
all_best_fitness = []
all_best_chromosomes = []

# Replacement strategy is Steady-state Replacement
for generation in range(gen):
    new_generation = []
    while len(new_generation) != 100:
        Pc = random.random()
        selection1 = roulette_wheel_selection(fitness)
        selection2 = roulette_wheel_selection(fitness)
        if Pc <= crossover_probability:
            offsprings = crossover(population[selection1], population[selection2])
            new_generation.extend(offsprings)
        else:
            new_generation.append(population[selection1])
            new_generation.append(population[selection2])
    for ind in range(100):
        Pm = random.random()
        if Pm <= mutation_probability:
            mutation(new_generation[ind])
    fitness = calculate_fitness(new_generation)
    new_fit = best_fit(fitness)
    all_best_fitness.append(fitness[new_fit])
    all_best_chromosomes.append(new_generation[new_fit])

    # Storing all generations progress in a file
    file2.write("         Generation " + str(generation + 1) + "              Fitness \n")
    file2.write("===========================================\n")
    for ind in range(len(new_generation)):
        file2.write(str(new_generation[ind]) + "      " + str(fitness[ind]) + "\n")
    file2.write("\nBest Fit in the Generation : " + "\n")
    file2.write(str(new_generation[new_fit]) + "      " + str(fitness[new_fit]) + "\n")
    file2.write("********************************************\n\n")

    population = new_generation


file2.close()

# Storing The best individuals and optimal solution in a file
final_file = open("final solution.txt", "w")
final_file.write("                        Best Chromosomes            Fitness\n")
final_file.write("==========================================================\n")
for ind in range(len(all_best_fitness)):
    final_file.write("Generation " + str(ind+1) + " :  " + str(all_best_chromosomes[ind]) + "      " + str(all_best_fitness[ind]) + "\n")
optimal = best_fit(all_best_fitness)
final_file.write("\n\nOptimal Solution :\n ")
final_file.write("Generation " + str(optimal+1) + " :  " + str(all_best_chromosomes[optimal]) + "      " + str(all_best_fitness[optimal]) + "\n")
final_file.close()

print("3 Files Created with the following specifications :")
print("initial generation.txt => The initial population and fitness")
print("generations progress.txt => The progress of all the generations with its fitness")
print("final solution.txt => The best chromosome in each generation and its fitness, the final optimal solution happened in all generations")
