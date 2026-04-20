from Sudoku_Board_Class import SudokuBoard

def neighborhood():
    '''
    This function will explore the nearby solutions, using the ideas from particle
    swarm algorithm. Combining a random change with the best fitness board.
    :return:
    '''


def main_pso():
    '''
    This is the main function of Particle Swarm Optimization algoirthm. Here is where we will
    want to run everything. THe idea is to initialize n boards by using the boardstring we get from
    mohan and then randomly filling the n boards. ANd then for p cycles we will, get the fitness scores
    of all boards, we then change each board randmly first and then use the best fitness board to
    influence a new change, this is the "particle swarm" part of the implementation
    :return:
    '''

#This is just testing sudokuboard class functions
BoardString = input()
board = SudokuBoard(BoardString)
print(board)

board.random_fill()
print(board)

board.fitness_eval()
print(board.fitness)

