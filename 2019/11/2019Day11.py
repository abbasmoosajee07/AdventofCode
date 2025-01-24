"""Advent of Code - Day 11, Year 2019
Solution Started: Jan 23, 2025
Puzzle Link: https://adventofcode.com/2019/day/11
Solution by: abbasmoosajee07
Brief: [Intcode Painting Robots]
"""

#!/usr/bin/env python3

import os, re, copy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = list(map(int, input_data))

cpu_p1 = Intcode_CPU(input_program, init_inputs=1, debug=False)
cpu_p1.process_program()
output = cpu_p1.get_result('output')
print("Output:", sum(output))
