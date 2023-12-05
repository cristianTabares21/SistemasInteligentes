# Desarrollado por: Cristian Tabares y Jean Paul Gonzalez.

import random

# Asignación de valores a los posibles movimientos según el PDF.
movements = {
    0: "Right",
    1: "Up",
    2: "Left",
    3: "Down"
}

# Definición del estado objetivo, en este caso una matriz 4x4.
goal_state = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]  # El 0 representa el espacio en blanco.
]

# Estado inicial (en desorden).
initial_state = [
    [3, 2, 9, 10],
    [6, 11, 15, 8],
    [1, 0, 4, 12],
    [7, 13, 14, 5]
]

goal_positions = {}  # Representan las posiciones objetivo de cada una de las fichas, por ejemplo: La ficha "1" su posición objetivo es: (0,0)
for i in range(4):
    for j in range(4):
        goal_positions[goal_state[i][j]] = (i, j)  # Coordenada i,j para cada ficha del tablero.

# Función para generar un individuo.
def generateIndividual(length):
    return [random.randint(0, 3) for _ in range(length)]  # El individuo representa un conjunto de posibles acciones.

# Función para generar una población.
def generatePopulation(population_size, length):
    return [generateIndividual(length) for _ in range(population_size)]  # Lista de individuos.

# Función para encontrar el espacio en blanco dentro del tablero.
def findBlankSpace(current_state):
    blank_position = None
    for i in range(4):
        for j in range(4):
            if current_state[i][j] == 0:
                blank_position = (i, j)
                break
    return blank_position

# Función que calcula la aptitud de ese individuo dado, utilizando distancia Manhattan.
def fitness(individual):
    current_state = [row.copy() for row in initial_state]  # Realizamos una copia profunda del estado inicial para poder modificarlo.

    # Inicializamos la variable que obtendrá la distancia Manhattan al final.
    total_distance = 0

    for move in individual:  # Cada movimiento que realiza el individuo.
        direction = movements[move]  # Obtenemos la dirección del movimiento: Up, Right, Left, Down.
        blank_space = findBlankSpace(current_state)

        # En cada movimiento, se verifica su dirección y que el movimiento se haga dentro del tablero.
        if direction == "Up" and blank_space[0] > 0:
            current_state[blank_space[0]][blank_space[1]], current_state[blank_space[0] - 1][blank_space[1]] = current_state[blank_space[0] - 1][blank_space[1]], current_state[blank_space[0]][blank_space[1]]
        elif direction == "Down" and blank_space[0] < 3:
            current_state[blank_space[0]][blank_space[1]], current_state[blank_space[0] + 1][blank_space[1]] = current_state[blank_space[0] + 1][blank_space[1]], current_state[blank_space[0]][blank_space[1]]
        elif direction == "Left" and blank_space[1] > 0:
            current_state[blank_space[0]][blank_space[1]], current_state[blank_space[0]][blank_space[1] - 1] = current_state[blank_space[0]][blank_space[1] - 1], current_state[blank_space[0]][blank_space[1]]
        elif direction == "Right" and blank_space[1] < 3:
            current_state[blank_space[0]][blank_space[1]], current_state[blank_space[0]][blank_space[1] + 1] = current_state[blank_space[0]][blank_space[1] + 1], current_state[blank_space[0]][blank_space[1]]

    # Calculamos la distancia Manhattan total después de realizar todos los movimientos.
    for i in range(4):
        for j in range(4):
            goal_position = goal_positions[current_state[i][j]]
            distance = abs(goal_position[0] - i) + abs(goal_position[1] - j)
            total_distance += distance

    return total_distance  # Retorna la distancia Manhattan total como aptitud

# Función que se encarga de seleccionar los padres, aplicando el método de torneo.
def selection(tournament_size, population, fitnesses):
    selected = []
    
    for _ in range(2):  # Se seleccionan dos padres.
        # Se escogen al azar los individuos que participarán en el torneo.
        contenders = random.sample(list(zip(population, fitnesses)), tournament_size)
        # El ganador es aquel individuo con la mejor aptitud.
        winner = min(contenders, key=lambda x: x[1])[0]
        selected.append(winner)
    return selected  # Se retornan los padres seleccionados.

# Función que se encarga de realizar el cruce entre los dos padres.
def crossover(parents):
    # Definimos un pivote para realizar el cruce.
    pivot = random.randint(0, len(parents[0]))
    
    # Creamos dos nuevos hijos mezclando ambas partes de los padres.
    child1 = parents[0][:pivot] + parents[1][pivot:]
    child2 = parents[1][:pivot] + parents[0][pivot:]
    
    return [child1, child2]  # Retornamos los dos nuevos hijos.

# Función que se encarga de mutar alguno de los individuos de la población.
def mutation(individual, mutation_rate):
    # Se recorre cada movimiento del individuo.
    for i in range(len(individual)):
        # Respecto a la probabilidad de mutación, mutamos un movimiento del individuo.
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, 3)
    return individual

# Función principal
def geneticAlgorithm(individual_length, population_size, tournament_size, mutation_rate, max_generations):
    
    # Generamos la población inicial.
    population = generatePopulation(population_size, individual_length)

    # Realizamos la evolución de la población durante varias generaciones.
    for generation in range(max_generations):
        # Calculamos la aptitud de cada uno de los individuos en la población.
        fitnesses = [fitness(individual) for individual in population]
        
        # Verificamos si alguno de los individuos ha alcanzado el estado objetivo.
        for individual, fitnessInd in zip(population, fitnesses):
            if fitnessInd == 0: 
                print("Alcanzo el estado objetivo")
                return individual  # Retornamos ese individuo que alcanzó el estado objetivo
        
        # Si ningun individuo alcanzó el estado objetivo, creamos una nueva población.
        new_population = []
        while len(new_population) < population_size:
            # Seleccionamos dos padres para la reproducción.
            parents = selection(tournament_size, population, fitnesses)
            # Se crean dos nuevos hijos mediante el cruce de los padres.
            children = crossover(parents)
            # Se mutan los hijos
            children = [mutation(child, mutation_rate) for child in children]
            # Se agregan los hijos a la nueva población.
            new_population.extend(children)
        
        # La nueva población pasa a ser la población actual.
        population = new_population
    
    # Se devuelve el mejor individuo de la última generación si no se alcanzó el estado objetivo.
    fitnesses = [fitness(individual) for individual in population]
    best_individual = min(zip(population, fitnesses), key=lambda x: x[1])[0]
    return best_individual

# Parámetros del algoritmo genético
population_size = 100
individual_length = 50
tournament_size = 5
mutation_rate = 0.1
max_generations = 100

# Llamamos a la función geneticAlgorithm para resolver el problema
best_individual = geneticAlgorithm(individual_length, population_size, tournament_size, mutation_rate, max_generations)

# Imprimimos la mejor solución encontrada
print(best_individual)