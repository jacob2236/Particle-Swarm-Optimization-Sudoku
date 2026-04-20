import numpy as np
import random as r

class SudokuBoard:
    def __init__(self, BoardString):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.givens = [] # we do not want the numbers in these indices to change
        self.fitness = 69420
        self.assign_board(BoardString)

        self.valid_vals = [ i for i in range(1,10)]

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

        self.fitness = fitness

    #creates one string that is then printed to screen
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

        return pboard
