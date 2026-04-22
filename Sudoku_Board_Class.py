import numpy as np
import random as r
import copy

class SudokuBoard:
    def __init__(self, BoardString):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.givens = [] # we do not want the numbers in these indices to change
        self.fitness = 69420
        self.best_fitness = 69420
        self.assign_board(BoardString)

        self.valid_vals = [ i for i in range(1,10)]
        self.local_best = None

    def _unused_vals_in_row(self, row):
        return [ i for i in range(len(self.board[row])) if self.board[row][i] not in self.valid_vals ]
        
    def random_fill(self):
        '''
        This function will randomly fill a sudoku board with values, keeping row consistency,
        meaning that each row will always be correct (ie no duplicates)
        :param SudokuBoard:
        :return SudokuBoard:
        '''

        for i in range(len(self.board)):
            unused = self._unused_vals_in_row(i)
            r.shuffle(unused)
            x = 0

            for j in range(len(self.board[i])):
                if self.board[i][j] > 0:
                    continue

                self.board[i][j] = unused[x]
                x += 1

        self.fitness_eval()

    def assign_board(self, BoardString):
        for i in range(9):
            for j in range(9):
                if BoardString[9*i + j] == '*':
                    self.board[i][j] = 0
                else:
                    self.board[i][j] = int(BoardString[9*i + j])
                    self.givens.append((i,j))

    def fitness_eval(self):
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

        if fitness < self.best_fitness:
            self.local_best = copy.deepcopy(self.board)
            self.best_fitness = fitness

        self.fitness = fitness

    def merge_board(self, other_board, weight):

        for _ in range(weight):
            i, j = r.randint(0,8), r.randint(0,8) 

            if (i, j) in self.givens:
                continue

            self.board[i][j] = other_board[i][j]

        self.fitness_eval()

    def merge_local_best(self, weight):
        self.merge_board(self.local_best, weight)

    def _mutate_row(self, i, chance):
        while True:
            if r.randint(0, 100) > chance:
                return

            j =  r.randint(0,8) 

            while (i,j) in self.givens:
                j = r.randint(0,8) 

            y = r.randint(0,8) 

            while (i,y) in self.givens:
                y = r.randint(0,8) 

            tmp = self.board[i][j]
            self.board[i][j] = self.board[i][y]
            self.board[i][y] = tmp

    def mutate_board(self, chance):
        for i in range(9):
            self._mutate_row(i, chance)

        self.fitness_eval()

    def __str__(self):
        pboard = ""
        for i in range(9):
            if i!=0 and i%3==0:
                pboard += "-----------------------------\n"
            for j in range(9):
                if j!=0 and j%3==0:
                    pboard += "|"
                pboard += f" {self.board[i][j]} "
            pboard += "\n"

        return pboard + f"fitness: {self.fitness}\n"

