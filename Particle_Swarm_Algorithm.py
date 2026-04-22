from Sudoku_Board_Class import SudokuBoard
import copy

GENERATION_COUNT = 1000
PARTICLE_COUNT = 300

GLOBAL_WEIGHT = 10
LOCAL_WEIGHT = 100

MUTATE_CHANCE = 40

def get_global_best(particle_arr):
    best = particle_arr[0]

    for p in particle_arr:
        if p.fitness < best.fitness:
            best = p

    return best

def global_travel(arr, g_best):
    for p in arr:
        p.merge_board(g_best.board, GLOBAL_WEIGHT)

def local_travel(arr):
    for p in arr:
        p.merge_local_best(LOCAL_WEIGHT)

def mutate_particles(arr, g_best):
    for p in arr:
        if p == g_best:
            continue

        p.mutate_board(MUTATE_CHANCE)

def init_particles(board_string):
    arr = [ SudokuBoard(board_string) for _ in range(PARTICLE_COUNT) ]

    for p in arr:
        p.random_fill()

    return arr

def main_pso(board_string):
    particles = init_particles(board_string)
    g_best = get_global_best(particles)

    for _ in range(GENERATION_COUNT):
        local_travel(particles)
        global_travel(particles, g_best)
        mutate_particles(particles, g_best)

        gen_best = get_global_best(particles)

        if gen_best.fitness < g_best.fitness:
            g_best = copy.deepcopy(gen_best)

        print(f"Generation global best fitness: {gen_best.fitness}")
        print(f"Global best fitness: {g_best.fitness}\n")

# this is just testing sudokuboard class functions
board_string = input()
main_pso(board_string)

