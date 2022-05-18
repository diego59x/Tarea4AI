import numpy as np
from datetime import datetime
from time import time
import turtle


# Function to compute the distance between two points
def distance_between_cities(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5


def compute_city_distance_names(city_a, city_b, ciudades):
    return distance_between_cities(ciudades[city_a], ciudades[city_b])


# First step: Create the first population set
def genesis(city_list, poblacion):

    grupo_poblacion = []
    for i in range(poblacion):
        # Randomly generating a new solution
        sol_i = city_list[
            np.random.choice(
                list(range(num_ciudades)), num_ciudades, replace=False
            )
        ]
        grupo_poblacion.append(sol_i)
    return np.array(grupo_poblacion)


def fit_evaluation(city_list, ciudades):
    total = 0
    for i in range(num_ciudades-1):
        a = city_list[i]
        b = city_list[i+1]
        total += compute_city_distance_names(a, b, ciudades)
    return total


def get_all_fitnes(grupo_poblacion, ciudades):
    fit_poblacion_ciudad = np.zeros(poblacion)

    # Looping over all solutions computing the fitness for each solution
    for i in range(poblacion):
        fit_poblacion_ciudad[i] = fit_evaluation(grupo_poblacion[i], ciudades)

    return fit_poblacion_ciudad


def father_selection(grupo_poblacion, fit_poblacion_ciudad):
    total_fit = fit_poblacion_ciudad.sum()
    prob_list = fit_poblacion_ciudad/total_fit

    # Notice there is the chance that a progenitor. mates with oneself
    progenitor_list_a = np.random.choice(list(range(len(grupo_poblacion))), len(grupo_poblacion),p=prob_list, replace=True)
    progenitor_list_b = np.random.choice(list(range(len(grupo_poblacion))), len(grupo_poblacion),p=prob_list, replace=True)

    progenitor_list_a = grupo_poblacion[progenitor_list_a]
    progenitor_list_b = grupo_poblacion[progenitor_list_b]

    return np.array([progenitor_list_a, progenitor_list_b])


def fathers_pair(prog_a, prog_b):
    offspring = prog_a[0:5]

    for city in prog_b:

        if not city in offspring:
            offspring = np.concatenate((offspring,[city]))

    return offspring

def population_pair(padres):
    nueva_poblacion = []
    for i in range(padres.shape[1]):
        prog_a, prog_b = padres[0][i], padres[1][i]
        offspring = fathers_pair(prog_a, prog_b)
        nueva_poblacion.append(offspring)

    return nueva_poblacion


def mutate_child(offspring):
    for q in range(int(num_ciudades*mutation_rate)):
        a = np.random.randint(0,num_ciudades)
        b = np.random.randint(0,num_ciudades)

        offspring[a], offspring[b] = offspring[b], offspring[a]

    return offspring


def mutate_population(nueva_poblacion):
    poblacion_mutada = []
    for offspring in nueva_poblacion:
        poblacion_mutada.append(mutate_child(offspring))
    return poblacion_mutada

# Parameters
num_ciudades = 5
poblacion = 10
mutation_rate = 0.3

# Generating a list of coordenades representing each city
coordenadas = [[x,y] for x,y in zip(np.random.randint(0,100,num_ciudades),np.random.randint(0,100,num_ciudades))]
nombres_list = ['Berlin', 'London', 'Moscow', 'Barcelona', 'Rome']
nombres = np.array(nombres_list)
ciudades = { x:y for x,y in zip(nombres,coordenadas)}

# Generating all the lists and sets
grupo_poblacion = genesis(nombres, poblacion)
fit_poblacion_ciudad = get_all_fitnes(grupo_poblacion,ciudades)
padres = father_selection(grupo_poblacion,fit_poblacion_ciudad)
nueva_poblacion = population_pair(padres)
poblacion_mutada = mutate_population(nueva_poblacion)

start = time()

# Best solution iterations
mejor_solucion = [-1,np.inf,np.array([])]
for i in range(10000):
    if i%100==0: print(i, fit_poblacion_ciudad.min(), fit_poblacion_ciudad.mean(), datetime.now().strftime("%d/%m/%y %H:%M"))
    fit_poblacion_ciudad = get_all_fitnes(poblacion_mutada,ciudades)

    # Saving the best solution
    if fit_poblacion_ciudad.min() < mejor_solucion[1]:
        mejor_solucion[0] = i
        mejor_solucion[1] = fit_poblacion_ciudad.min()
        mejor_solucion[2] = np.array(poblacion_mutada)[fit_poblacion_ciudad.min() == fit_poblacion_ciudad]

    padres = father_selection(grupo_poblacion,fit_poblacion_ciudad)
    nueva_poblacion = population_pair(padres)

    poblacion_mutada = mutate_population(nueva_poblacion)

end = time()

# Print the solution
res = list(list(mejor_solucion[2])[0])
print("\nSolución: ", res)
print("Tiempo de ejecución: ", end-start)

colors = ['red', 'blue', 'green', 'yellow', 'orange'][:len(nombres)]
for r, c in zip(nombres_list, colors):
    print(r, " (", c, ")")

scale = 3
wn = turtle.Screen()
t = turtle.Turtle()
t.up()
t.speed(0)
for c, col in zip(coordenadas, colors):
    t.goto(c[0]*scale, c[1]*scale)
    t.dot(20, col)

for n in res:
    i = nombres_list.index(n)
    c = coordenadas[i]
    t.goto(c[0]*scale, c[1]*scale)

    t.speed(1)
    t.down()

turtle.done()
