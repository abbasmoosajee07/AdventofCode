# Advent of Code - Day 5, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/5
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer P2 (D5)]

#!/usr/bin/env python3

import os, re, copy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

# Read and sort input data into a grid
with open(D05_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = list(map(int, input_data))

cpu_p1 = Intcode_CPU(input_program, inputs=1)
cpu_p1.process_program()
output_p1 = cpu_p1.get_result('output')
diagnostic_code =  next((x for x in output_p1 if x != 0), None)
print("Part 1:", diagnostic_code)