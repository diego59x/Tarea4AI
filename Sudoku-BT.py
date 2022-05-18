import time

iteraciones = 0

def isValid(puzzle, i, row, col):
    rows = puzzle[int(row)]
    column = [puzzle[r][col] for r in range(0,9,1)]
    if i in rows:
        return False
    if i in column:
        return False
    SquareRow = (row // 3)*3
    squareColumn = (col // 3)*3
    Square = [puzzle[y][z] for y in range(SquareRow, SquareRow+3) for z in range(squareColumn, squareColumn+3)]
    
    if i in Square:
        return False
    return True


def find(puzzle):
    for i in range(0,9,1):
        for j in range(0,9,1):
            if puzzle[i][j]==0:
                return i,j
    return None


def solveSudoku(sudoku):
    finds = find(sudoku)
    global iteraciones
    if not finds:
        return True
    else:
        i, j = finds

    for x in range(1,10):
        iteraciones += 1
        if isValid(sudoku, x, i, j):
            sudoku[i][j] = x

            if solveSudoku(sudoku):
                return True

            sudoku[i][j] = 0
    
    return False

file = 'sudoku.txt'

with open(file) as file:
    lines = [line.rstrip() for line in file]

file.close()

sudoku = []
for i in range(0, int(lines[0])):
    row = []
    for j in range(0, int(lines[0])):
        row.append(0)
    sudoku.append(row)

for i in range(2, int(lines[1]) + 2):
    casilla = lines[i].split()
    sudoku[int(casilla[0])-1][int(casilla[1])-1] = int(casilla[2])

start_time = time.time()

solveSudoku(sudoku)

print("Tiempo de ejecucion: %s" % (time.time() - start_time) + " segundos\n")

for row in sudoku:
    print(*row)

print("\nNumero de iteraciones: ",iteraciones)
           
