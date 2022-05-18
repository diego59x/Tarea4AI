# Genetic Algorithm
# Abraham Gutierrez
# Diego Alvarez
# Walter Saldaña
# Javier Cotto
from math import sqrt
from random import shuffle, randint
from Utils import *
import time

def sudoku(sudoku_grid, population_size, selection_rate, max_generations_count, mutation_rate):

    # square root of the sudoku 9x9
    SquareSize = int(sqrt(len(sudoku_grid)))
    
    # Create an empty array representing a sudoku
    def clean_grid(elem_generator=None):
        return [
            [
                (None if elem_generator is None else elem_generator(i, j))
                for j in range(len(sudoku_grid))
            ] for i in range(len(sudoku_grid))
        ]
    # Copy the array of sudoku
    def duplicate_grid(grid):
        return clean_grid(lambda i, j: grid[i][j])

    # This is a defensive strategy if the input argument changes
    sudoku_grid = duplicate_grid(sudoku_grid)

    # Generates numbers 
    def same_sub_grid_indexes(i, j, itself=True):

        for k in range(len(sudoku_grid)):
            if k == j and not itself:
                continue

            yield (i, k)
    # Fill the grid with pencil marking method
    def fill_cells_pencil():

        track_grid = clean_grid(lambda *args: [val for val in range(1, len(sudoku_grid) + 1)])

        # Mark the element
        def pencil_method(i, j):

            # Remove same cell of a grid 
            for a, b in same_sub_grid_indexes(i, j, itself=False):
                try:
                    track_grid[a][b].remove(sudoku_grid[i][j])
                except (ValueError, AttributeError) as e:
                    pass

            # Remove same cell of a row
            for a, b in same_row_indexes(sudoku_grid, i, j, SquareSize, itself=False):
                try:
                    track_grid[a][b].remove(sudoku_grid[i][j])
                except (ValueError, AttributeError) as e:
                    pass

            # Remove same cell of a column
            for a, b in same_column_indexes(sudoku_grid, i, j, SquareSize, itself=False):
                try:
                    track_grid[a][b].remove(sudoku_grid[i][j])
                except (ValueError, AttributeError) as e:
                    pass
        # Verify elements None
        for i in range(len(sudoku_grid)):
            for j in range(len(sudoku_grid)):
                if sudoku_grid[i][j] is not None:
                    pencil_method(i, j)

        while True:
            any_change_in_grid = False

            for i in range(len(sudoku_grid)):
                for j in range(len(sudoku_grid)):
                    if track_grid[i][j] is None:
                        continue

                    if len(track_grid[i][j]) == 0:
                        raise Exception('El sudoku no tiene solucion')
                    elif len(track_grid[i][j]) == 1:
                        sudoku_grid[i][j] = track_grid[i][j][0]
                        pencil_method(i, j)

                        track_grid[i][j] = None

                        any_change_in_grid = True

            if not any_change_in_grid:
                break

        return sudoku_grid

    # Generates population
    def generate_population():

        candidates = []
        for k in range(population_size):
            candidate = clean_grid()
            for i in range(len(sudoku_grid)):
                shuffled_sub_grid = [n for n in range(1, len(sudoku_grid) + 1)]
                shuffle(shuffled_sub_grid)

                for j in range(len(sudoku_grid)):
                    if sudoku_grid[i][j] is not None:
                        candidate[i][j] = sudoku_grid[i][j]

                        shuffled_sub_grid.remove(sudoku_grid[i][j])

                for j in range(len(sudoku_grid)):
                    if candidate[i][j] is None:
                        candidate[i][j] = shuffled_sub_grid.pop()

            candidates.append(candidate)

        return candidates
    # Fitness of the population for the grid
    def fitness(grid):

        row_duplicates_count = 0

        # calculate rows duplicates
        for a, b in same_column_indexes(sudoku_grid, 0, 0, SquareSize):
            row = list(get_cells_from_indexes(grid, same_row_indexes(sudoku_grid, a, b, SquareSize)))

            row_duplicates_count += len(row) - len(set(row))

        return row_duplicates_count
    # Return the best fitness of each candidate
    def selection(candidates):

        index_fitness = []
        for i in range(len(candidates)):
            index_fitness.append(tuple([i, fitness(candidates[i])]))

        index_fitness.sort(key=lambda elem: elem[1])

        selected_part = index_fitness[0: int(len(index_fitness) * selection_rate)]
        indexes = [e[0] for e in selected_part]

        return [candidates[i] for i in indexes], selected_part[0][1]

    fill_cells_pencil()

    population = generate_population()
    best_fitness = None

    for i in range(max_generations_count):
        population, best_fitness = selection(population)

        if i == max_generations_count - 1 or fitness(population[0]) == 0:
            break

        shuffle(population)
        new_population = []

        while True:
            solution_a = None
            solution_b = None 

            try:
                solution_a = population.pop()
            except IndexError:
                break

            try:
                solution_b = population.pop()
            except IndexError:
                new_population.append(solution_b)
                break

            cross_point = randint(0, len(sudoku_grid) - 2)

            temp_sub_grid = solution_a[cross_point]
            solution_a[cross_point] = solution_b[cross_point + 1]
            solution_b[cross_point + 1] = temp_sub_grid

            new_population.append(solution_a)
            new_population.append(solution_b)

        # mutation
        for candidate in new_population[0:int(len(new_population) * mutation_rate)]:
            random_sub_grid = randint(0, 8)
            possible_swaps = []
            for grid_element_index in range(len(sudoku_grid)):
                if sudoku_grid[random_sub_grid][grid_element_index] is None:
                    possible_swaps.append(grid_element_index)
            if len(possible_swaps) > 1:
                shuffle(possible_swaps)
                first_index = possible_swaps.pop()
                second_index = possible_swaps.pop()
                tmp = candidate[random_sub_grid][first_index]
                candidate[random_sub_grid][first_index] = candidate[random_sub_grid][second_index]
                candidate[random_sub_grid][second_index] = tmp

        population.extend(new_population)

    return population[0], best_fitness


try:
    with open("sudoku_1.txt", "r") as input_file:
        file_content = input_file.read()
        file_lines = file_content.split('\n')
        sudoku_grid = [[] for i in range(len(file_lines))]
        sqrt_n = int(sqrt(len(file_lines)))
        for j in range(len(file_lines)):
            line_values = [(int(value) if value != ' ' else None) for value in file_lines[j].split(' ')]
            for i in range(len(line_values)):
                sudoku_grid[
                    int(i / sqrt_n) +
                    int(j / sqrt_n) * sqrt_n
                    ].append(line_values[i])
        try:
            start = time.time()

            solution, best_fitness = sudoku(
                    sudoku_grid,
                    population_size=1000,
                    selection_rate=100,
                    max_generations_count=100,
                    mutation_rate=0
                )
            end = time.time()

            output_str = "Valor fitness: " + str(best_fitness) + '\n\n'
            for a, b in same_column_indexes(solution, 0, 0, sqrt_n):
                row = list(get_cells_from_indexes(solution, same_row_indexes(solution, a, b, sqrt_n)))

                output_str += " ".join([str(elem) for elem in row]) + '\n'
            output_str = output_str
            print("Time to solve: ", str( end - start))
            print(output_str[:-1])

        except:
            exit('Sudoku sin solucion')
except FileNotFoundError:
    exit("Archivo no encontrado")
