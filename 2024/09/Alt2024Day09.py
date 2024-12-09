"""Advent of Code - Day 9, Year 2024
Solution Started: Dec 9, 2024
Puzzle Link: https://adventofcode.com/2024/day/9
Solution by: abbasmoosajee07
Brief: [Free up Disk Space]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D09_file = "Day09_input.txt"
D09_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D09_file)

# Read and sort input data into a grid
with open(D09_file_path) as file:
    input_data = file.read().strip().split('\n')[0]

def calculate_checksum(file) -> list:
    checksum = 0
    for pos, num in enumerate(file):
        checksum += (pos * int(num))
    return checksum

def create_file(file_str) -> str:
    id = 0
    expanded_file = []
    file_list = list(file_str)
    for pos, space in enumerate(file_list):
        space = int(space)
        if pos % 2 == 0:
            add_file = [f"{id}"] * space
            id += 1
        else:
            add_file = ['.'] * space
        expanded_file.append(add_file)

    return expanded_file

def free_disk_space(file_list) -> list:
    flat_file = [item for sublist in file_list for item in sublist]

    defragmented_file = copy.deepcopy(flat_file)
    empty_spaces = [index for index, value in enumerate(flat_file) if value == '.']
    full_file = [value for index, value in enumerate(flat_file) if value != '.']

    for pos in empty_spaces:
        type = defragmented_file[pos]
        last_pos = full_file[-1]
        defragmented_file[pos] = last_pos
        full_file = full_file[:-1]
    defragmented_file = defragmented_file[:-len(empty_spaces)]
    return calculate_checksum(defragmented_file)

fragmented_file = create_file(input_data)
ans_p1 = free_disk_space(fragmented_file)
print("Part 1:", ans_p1)

def reorganize_files(disk_code) -> int:
    """
    Reorganize files based on available free spaces and calculate the final result.
    """
    d = {}
    frees = []
    counter = 0

    # Create the file representation from disk code
    for i, r in enumerate(disk_code):
        start, end = counter, counter + r
        if i % 2 == 0:
            d[i//2] = (start, end)
        elif r > 0:
            frees.append((start, end))
        counter += r

    # Two pointers to track the files and the free gaps
    idx_ptr = max(d.keys())

    while idx_ptr >= 0:
        file_start, file_end = d[idx_ptr]
        file_len = file_end - file_start

        free_ptr = 0
        while free_ptr < len(frees):
            gap_start, gap_end = frees[free_ptr]
            if gap_start >= file_start:
                break

            gap_len = gap_end - gap_start
            if file_len <= gap_len:
                frees.pop(free_ptr)

                # Move file to the gap
                new_file_start, new_file_end = gap_start, gap_start + file_len
                new_gap_start, new_gap_end = new_file_end, gap_end

                # Update file and gap positions
                d[idx_ptr] = (new_file_start, new_file_end)
                if new_gap_start != new_gap_end:
                    frees.insert(free_ptr, (new_gap_start, new_gap_end))
                break
            else:
                free_ptr += 1

        idx_ptr -= 1

    # Calculate the result
    result = 0
    for k, (start, end) in d.items():
        result += sum(k * i for i in range(start, end))
    return result, d

with open(D09_file_path) as f:
    disk_code = [int(i) for i in "".join(x.strip() for x in f)]

# Reorganize and calculate the checksum for part 2
ans_p2, file = reorganize_files(disk_code)
print("Part 2:", ans_p2)
print(file)