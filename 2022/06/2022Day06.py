"""Advent of Code - Day 6, Year 2022
Solution Started: Nov 29, 2024
Puzzle Link: https://adventofcode.com/2022/day/6
Solution by: abbasmoosajee07
Brief: [Strings]
"""

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path) as file:
    input_data = file.read().strip().split('\n')
    string_list = list(input_data[0])

def find_consecutive_unique(string_list, group = 1):
    for pos in range(len(string_list) - group - 1):  # We only need to go up to len - 3
        # Check if the next four characters are distinct
        if len(set(string_list[pos:pos+group])) == group:
            return pos + group
            break
ans_p1 = find_consecutive_unique(string_list, group = 4)
print("Part 1:", ans_p1)
ans_p2 = find_consecutive_unique(string_list, group = 14)
print("Part 2:", ans_p2)
