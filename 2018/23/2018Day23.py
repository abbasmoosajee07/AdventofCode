# Advent of Code - Day 23, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/23
# Solution by: [abbasmoosajee07]
# Brief: [Tracking bots position]

#!/usr/bin/env python3

import os, subprocess
# File paths
solution_p1 = "2018Day23_P1.py"
solution_path_p1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p1)

solution_p2 = "2018Day23_P2.py"
solution_path_p2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p2)

# Run Python script
subprocess.run(["python", solution_path_p1], check=True)

# Run Ruby script
# subprocess.run(["python", solution_path_p2], check=True)

