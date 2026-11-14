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

def geometricCrossover3Parents(parent1,parent2,parent3):
    parent1weight,parent2weight,parent3weight = 0.2,0.4,0.4
    temp1 = copy.deepcopy(parent1)
    temp2 = copy.deepcopy(parent2)
    temp3 = copy.deepcopy(parent3)
    mask = []

    for i in range(9):
        mask.clear()
        for j in range(9):
            random.seed(time.time())
            random_int = random.random()
            if random_int < parent1weight:
                mask.append(1)
            elif random_int < parent2weight:
                mask.append(2)
            else:
                mask.append(3)

        for j in range(9):
            if mask[j] == 1:
                compare = temp1[i][j]
                if not compare == temp2[i][j]:
                    for n in range(9):
                        if temp2[i][n] == compare:
                            indextemp = temp2[i][j]
                            temp2[i][j] = temp2[i][n]
                            temp2[i][n] = indextemp
                            break

                if not compare == temp3[i][j]:
                    for n in range(9):
                        if temp3[i][n] == compare:
                            indextemp = temp3[i][j]
                            temp3[i][j] = temp3[i][n]
                            temp3[i][n] = indextemp
                            break

            if mask[j] == 2:
                compare = temp2[i][j]
                if not compare == temp1[i][j]:
                    for n in range(9):
                        if temp1[i][n] == compare:
                            indextemp = temp1[i][j]
                            temp1[i][j] = temp1[i][n]
                            temp1[i][n] = indextemp
                            break

                if not compare == temp3[i][j]:
                    for n in range(9):
                        if temp3[i][n] == compare:
                            indextemp = temp3[i][j]
                            temp3[i][j] = temp3[i][n]
                            temp3[i][n] = indextemp
                            break

            if mask[j] == 3:
                compare = temp3[i][j]
                if not compare == temp2[i][j]:
                    for n in range(9):
                        if temp2[i][n] == compare:
                            indextemp = temp2[i][j]
                            temp2[i][j] = temp2[i][n]
                            temp2[i][n] = indextemp
                            break

                if not compare == temp1[i][j]:
                    for n in range(9):
                        if temp1[i][n] == compare:
                            indextemp = temp1[i][j]
                            temp1[i][j] = temp1[i][n]
                            temp1[i][n] = indextemp
                            break

    return temp1

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


def mainPSO(BS):
    BoardString = BS
    Board = SudokuBoard(BoardString)
    print("Starting board:")
    Board.print()
    print()
    Board = randomFill(Board)
    Board.fitnessEval()



    num_generations = 200
    num_samples = 500
    samples = []

    for i in range(num_samples):
        new_board = SudokuBoard(BoardString)
        new_board = randomFill(new_board)
        new_board.fitnessEval()
        samples.append(new_board)
        #new_board.print()

    for i in range(num_generations):

        samples.sort(key=lambda b: b.fitness)

        '''for x in samples:
            print(x.fitness)
        print()'''

        for j in range(1,num_samples):
            best_parent,current_parent,current_best_parent = samples[0].board,samples[j].board,samples[j].p_best_board

            #temp_child = copy.deepcopy(PMXcrossover2Parents(current_best_parent,current_parent))
            #samples[j].board = copy.deepcopy(PMXcrossover2Parents(best_parent, temp_child))

            samples[j].board = copy.deepcopy(geometricCrossover3Parents(current_parent,best_parent,current_best_parent))

            random.seed(time.time())
            random_int = random.random()
            if random_int < .3:
                mutate(samples[j])

            samples[j].fitnessEval()

    return samples[0].fitness

boards = ["********1*******23**4**5******1*********3*6****7***58*****67****1***4***52*******",
          "***26*7*168**7**9*19***45**82*1***4***46*29***5***3*28**93***74*4**5**367*3*18***",
          "1**489**673*****4******1295**712*6**5**7*3**8**6*957**9146******2*****378**512**4",
          "*2*6*8***58***97******4****37****5**6*******4**8****13****2******98***36***3*6*9*",
          "***6**4**7****36******91*8***********5*18***3***3*6*45*4*2***6*9*3*******2****1**",
          "2**3*****8*4*62**3*138**2******2*39*5*7***621*32**6****2***914*6*125*8*9*****1**2",
          "*2**********6****3*74*8*********3**2*8**4**1*6**5*********1*78*5****9**********4*",
          "***26*7*168**7**9*19***45**82*1***4***46*29***5***3*28**93***74*4**5**367*3*18***",
          "45*********2*7*63********28***95*****86***2***2*6**75*******476*7**45*****8**9***",
          "*1************19*5*64*2*3***4**1******13*64******7**9***5*4*62*8*92************5*"]
avg = 0
for b in boards:
    avg += mainPSO(b)
    print(f"average for this iteration {avg}\n")

avg /= len(boards)
print(f"average for the whole algorithm  {avg}")