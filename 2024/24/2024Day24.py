"""Advent of Code - Day 24, Year 2024
Solution Started: Dec 24, 2024
Puzzle Link: https://adventofcode.com/2024/day/24
Solution by: abbasmoosajee07
Brief: [Building Circuits]
"""

#!/usr/bin/env python3

import os
import subprocess
import time

start_time = time.time()

# File paths
solution_p1 = "2024Day24_P1.py"
solution_path_p1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p1)

solution_p2 = "2024Day24_P2.rb"
solution_path_p2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p2)

# Run Python script
subprocess.run(["python", solution_path_p1], check=True)

# Run Ruby script
subprocess.run(["ruby", solution_path_p2], check=True)

