"""Advent of Code - Day 6, Year 2022
Solution Started: Nov 29, 2024
Puzzle Link: https://adventofcode.com/2022/day/6
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path) as file:
    input_data = file.read().strip().split('\n')
print(input_data)
