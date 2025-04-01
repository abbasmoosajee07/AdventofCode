"""Advent of Code - Day 25, Year 2019
Solution Started: Apr 1, 2025
Puzzle Link: https://adventofcode.com/2019/day/25
Solution by: abbasmoosajee07
Brief: [Intcode TextGame]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
start_time = time.time()

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)
# from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

# Read and sort input data into a grid
with open(D25_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_TextGame:
    def __init__(self, program: list[int]):
        self.game_software = program

text_game = Intcode_TextGame(input_program)

print(f"Execution Time = {time.time() - start_time:.5f}s")
