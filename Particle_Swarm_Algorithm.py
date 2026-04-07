from Sudoku_Board_Class import SudokuBoard
import random
import time
import copy


def randomFill(SudokuBoard):
    for i in range(9):
        possible_ints = list(range(1, 10))
        for x,y in SudokuBoard.givens:
            if x == i:
                possible_ints.remove(SudokuBoard.board[x][y])

        for j in range(9):
            if SudokuBoard.board[i][j] == 0:
                random.seed(time.time())
                choice = random.choice(possible_ints)
                SudokuBoard.board[i][j] = choice
                possible_ints.remove(choice)

    return SudokuBoard

def PMXcrossover2Parents(parent1,parent2):
    child = copy.deepcopy(parent2)

    for i in range(9):
        n = random.randint(0, 7)
        m = random.randint(n, 8)
        nums = list(range(1, 10))
        for j in range(n, m):
            child[i][j] = parent1[i][j]
            nums.remove(parent1[i][j])

        fixes = []
        for j in list(range(0, n)) + list(range(m,9)):
            if child[i][j] not in nums:
                fixes.append((i,j))
            else:
                nums.remove(child[i][j])

        for x,y in fixes:
            if child[x][y] in nums:
                nums.remove(child[x][y])
            else:
                random.seed(time.time())
                temp = random.choice(nums)
                nums.remove(temp)
                child[x][y] = temp


    return child

def mutate(sudokuboard):
    potential_swaps = []
    for i in range(9):
        potential_swaps.clear()
        for j in range(9):
            if (i,j) not in sudokuboard.givens:
                potential_swaps.append((i, j))
        random.seed(time.time())
        temp1x,temp1y = random.choice(potential_swaps)
        potential_swaps.remove((temp1x,temp1y))
        temp2x,temp2y = random.choice(potential_swaps)
        temp = sudokuboard.board[temp1x][temp1y]
        sudokuboard.board[temp1x][temp1y] = sudokuboard.board[temp2x][temp2y]
        sudokuboard.board[temp2x][temp2y] = temp
    return

def mainPSO():
    BoardString = "53**7****6**195***98****6*****6***34**8*3**17***2***6*6****28***419**5****8**79**"
    Board = SudokuBoard(BoardString)
    #Board.print()
    Board = randomFill(Board)
    Board.fitnessEval()
    Board.print()
    print(Board.p_best_board)

    num_generations = 100
    num_samples = 100
    samples = []

    for i in range(num_samples):
        new_board = SudokuBoard(BoardString)
        new_board = randomFill(new_board)
        new_board.fitnessEval()
        samples.append(new_board)
        #new_board.print()

    for i in range(num_generations):

        samples.sort(key=lambda b: b.fitness)

        for x in samples:
            print(x.fitness)
        print()

        for j in range(1,num_samples):
            best_parent,current_parent,current_best_parent = samples[0].board,samples[j].board,samples[j].p_best_board

            temp_child = copy.deepcopy(PMXcrossover2Parents(current_best_parent,current_parent))
            samples[j].board = copy.deepcopy(PMXcrossover2Parents(best_parent, temp_child))

            random.seed(time.time())
            random_int = random.random()
            if random_int < .3:
                mutate(samples[j])

            samples[j].fitnessEval()

mainPSO()