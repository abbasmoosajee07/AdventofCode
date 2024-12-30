"""Advent of Code - Day 12, Year 2023
Solution Started: Dec 28, 2024
Puzzle Link: https://adventofcode.com/2023/day/12
Solution by: abbasmoosajee07
Brief: [Filling the blanks]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read and sort input data into a grid
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list: list[str]) -> list[tuple]:
    spring_list = []
    for line in input_list:
        springs, damaged_groups = line.split(' ')
        damaged_sizes = tuple(map(int, damaged_groups.split(',')))
        spring_list.append((springs, damaged_sizes))
    return spring_list

def all_spring_arrangements(springs: str, groups: tuple) -> int:
    spring_order = 0
    print(f"{springs=} {groups=}")
    return spring_order

test_input = ['???.### 1,1,3', '.??..??...?##. 1,1,3', '?#?#?#?#?#?#?#? 1,3,1,6', '????.#...#... 4,1,1', '????.######..#####. 1,6,5', '?###???????? 3,2,1']

spring_list = parse_input(test_input)

total_combos = 0
for springs, group_order in spring_list:
    spring_combo = all_spring_arrangements(springs, group_order)
    total_combos += spring_combo
print("Part 1:", total_combos)