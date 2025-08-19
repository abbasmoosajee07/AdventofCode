# Advent of Code - Day 14, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/14
# Solution by: [abbasmoosajee07]
# Brief: [Perfect Chocolate Recipe]

import os
import subprocess

# File paths
solution_p1 = "2018Day14_P1.c"
solution_path_p1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p1)

solution_p2 = "2018Day14_P2.c"
solution_path_p2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p2)

# Output executables (compiled binaries)
exe_p1 = os.path.splitext(solution_path_p1)[0]  # "2017Day15_P1"
exe_p2 = os.path.splitext(solution_path_p2)[0]  # "2017Day15_P2"

# Compile both C programs
subprocess.run(["gcc", solution_path_p1, "-o", exe_p1], check=True)
subprocess.run(["gcc", solution_path_p2, "-o", exe_p2], check=True)

# Run both executables
subprocess.run([exe_p1], check=True)
subprocess.run([exe_p2], check=True)
