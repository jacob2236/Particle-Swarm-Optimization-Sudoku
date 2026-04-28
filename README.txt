# PSO Sudoku Solver (Finished Version)

## Files
- Sudoku_Board_Class.py -> board representation, fitness scoring, candidate/conflict helpers
- Particle_Swarm_Algorithm.py -> PSO-style search solver with tunable initialization diversity

## How to run
python3 Particle_Swarm_Algorithm.py

## Example with your variation
python3 Particle_Swarm_Algorithm.py --candidate-pool-size 9 --swarm-size 250 --iterations 2000

## Important knobs
- --swarm-size
  how many starting boards get created
- --candidate-pool-size
  controls how broad the starting fill is
  1 = very greedy
  9 = maximum variety / maximum possibility spread
- --iterations
  how long the swarm searches
- --inertia-swaps
  how many bad cells get changed per particle per iteration

## Board format
Use an 81-character line:
- digits 1-9 are givens
- *, 0, or . are blanks
