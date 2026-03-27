import numpy as np
import copy

class SudokuBoard:
    def __init__(self, BoardString):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.p_best_board = [[0 for _ in range(9)] for _ in range(9)]
        self.fitness = 69420
        self.p_best_fitness = 69420
        self.givens = [] # we do not want the numbers in these indices to change
        self.assignBoard(BoardString)

    def assignBoard(self, BoardString):
        for i in range(9):
            for j in range(9):
                if BoardString[9*i + j] == "*":
                    self.board[i][j] = 0
                else:
                    self.board[i][j] = int(BoardString[9*i + j])
                    self.givens.append((i,j))

    def fitnessEval(self):
        fitness = 0

        #checks row consistency
        for i in range(9):
            check = np.zeros(9)
            for j in range(9):
                if check[self.board[i][j] - 1] == 0:
                    check[self.board[i][j] - 1] = self.board[i][j]
                else:
                    fitness += 1

        #checks column consistency
        for i in range(9):
            check = np.zeros(9)
            for j in range(9):
                if check[self.board[j][i] - 1] == 0:
                    check[self.board[j][i] - 1] = self.board[j][i]
                else:
                    fitness += 1

        #checks block cosistency
        for i in range(3):
            for j in range(3):
                check = np.zeros(9)
                for n in range(3*i, 3*i+3):
                    for m in range(3*j, 3*j+3):
                        if check[self.board[n][m] - 1] == 0:
                            check[self.board[n][m] - 1] = self.board[n][m]
                        else:
                            fitness += 1

        self.fitness = fitness
        if self.fitness < self.p_best_fitness:
            self.p_best_fitness = self.fitness
            self.p_best_board = copy.deepcopy(self.board)


    #creates one string that is then printed to screen
    def print(self):
        pboard = ""
        for i in range(9):
            if i!=0 and i%3==0:
                pboard += "-----------------------------\n"
            for j in range(9):
                if j!=0 and j%3==0:
                    pboard += "|"
                pboard += f" {self.board[i][j]} "
            pboard += "\n"
        print(pboard)