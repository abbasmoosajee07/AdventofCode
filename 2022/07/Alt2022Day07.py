"""Advent of Code - Day 7, Year 2022
Solution Started: Nov 29, 2024
Puzzle Link: https://adventofcode.com/2022/day/7
Solution by: abbasmoosajee07
Brief: [File Tree]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split('\n')

def create_file_tree(command_list):
    sizes = defaultdict(int)
    stack = []

    for command in command_list:
        if command.startswith("$ ls") \
            or command.startswith("dir"):
            continue
        if command.startswith("$ cd"):
            destination = command.split()[2]
            if destination == "..":
                stack.pop()
            else:
                path = f"{stack[-1]}_{destination}" \
                    if stack else destination
                stack.append(path)
        else:
            size, _ = command.split()
            for path in stack:
                sizes[path] += int(size)

    required_size = 30000000 - (70000000 - sizes["/"])
    for size in sorted(sizes.values()):
        if size > required_size:
            break
    ans_p1 = sum(num for num in sizes.values() if num <= 100000)
    ans_p2 = size

    return ans_p1, ans_p2

ans_p1, ans_p2 = create_file_tree(input_data)
print("Part 1:", ans_p1)
print("Part 2:", ans_p2)
