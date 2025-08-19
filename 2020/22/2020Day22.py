# Advent of Code - Day 22, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Card Games, V1]

import os, subprocess
# File paths
solution_p1 = "2020Day22_P1.py"
solution_path_p1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p1)

solution_p2 = "2020Day22_P2.py"
solution_path_p2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p2)

# Run Python script
subprocess.run(["python", solution_path_p1], check=True)

# Run Ruby script
subprocess.run(["python", solution_path_p2], check=True)

