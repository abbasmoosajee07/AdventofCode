# Advent of Code - Day 6, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/6
# Solution by: [abbasmoosajee07]
# Brief: [Common Letter Columns]

import os
import re
import pandas as pd
import numpy as np
from collections import Counter

D6_file = 'Day06_input.txt'
D6_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D6_file)

with open(D6_file_path) as file:
    input = file.read()
    
input = input.splitlines()

text_list = []
for row in range(len(input)):
    row_text = input[row]
    characters = [char for char in row_text]
    text_list.append(characters)

text_array = np.array(text_list)

Part1_ans = []
Part2_ans = []

for col in range(text_array.shape[1]):
    text_col = text_array[:,col]
    count = Counter(text_col)

    most_common_letter = count.most_common(1)[0][0] # Get the most common 1 element
    Part1_ans.append(most_common_letter[0][0])

    least_common_letter = count.most_common()[-1][0] # Get the most common 1 element
    Part2_ans.append(least_common_letter[0][0])
    
print(f"Part 1: The puzzle answer is {Part1_ans}")
print(f"Part 2: The puzzle answer is {Part2_ans}")