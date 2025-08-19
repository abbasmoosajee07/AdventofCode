# Advent of Code - Day 22, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Battle Problem V2]


import os
import subprocess

# File paths

solution_p1 = "2015Day22_P1.rb"
solution_path_p1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p1)

solution_p2 = "2015Day22_P2.c"
solution_path_p2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p2)

# Output executables (compiled binaries)
exe_p2 = os.path.splitext(solution_path_p2)[0]  # "2017Day15_P1"

subprocess.run(["ruby", solution_path_p1], check=True)
subprocess.run(["gcc", solution_path_p2, "-o", exe_p2], check=True)
subprocess.run([exe_p2], check=True)
