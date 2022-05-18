# Genetic Algorithm
# Abraham Gutierrez
# Diego Alvarez
# Walter Saldaña
# Javier Cotto

# Generates indexes between columns
def same_column_indexes(problem_grid, i, j, N, itself=True):

    sub_grid_column = i % N
    cell_column = j % N

    for a in range(sub_grid_column, len(problem_grid), N):
        for b in range(cell_column, len(problem_grid), N):
            if (a, b) == (i, j) and not itself:
                continue

            yield (a, b)

# Generates indexes between rows
def same_row_indexes(problem_grid, i, j, N, itself=True):

    sub_grid_row = int(i / N)
    cell_row = int(j / N)

    for a in range(sub_grid_row * N, sub_grid_row * N + N):
        for b in range(cell_row * N, cell_row * N + N):
            if (a, b) == (i, j) and not itself:
                continue

            yield (a, b)

# Generates indexes between grid
def get_cells_from_indexes(grid, indexes):
    for a, b in indexes:
        yield grid[a][b]

