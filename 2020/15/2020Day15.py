# Advent of Code - Day 15, Year 2020
# Solution Started: Nov 21, 2024
# Puzzle Link: https://adventofcode.com/2020/day/15
# Solution by: [abbasmoosajee07]
# Brief: [Forming number sequences]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split(',')
    starting_no = [int(num) for num in input_data]

def get_second_last_occurrence_dict(ult, penul, last_value):
    # Function to find the second last occurrence using ult and penul dictionaries
    if last_value in penul and penul[last_value] != 0:
        return penul[last_value]
    return None

def create_number_sequence_v2(starting_no, total):
    # Initialize values
    ult = {}
    penul = {}
    turn = 1
    
    # Seed the tables
    for num in starting_no:
        ult[num] = turn
        penul[num] = 0
        turn += 1

    target = starting_no[-1]
    while turn <= total:
        second_last_idx = get_second_last_occurrence_dict(ult, penul, target)

        if second_last_idx is None:  # First time spoken
            target = 0
            penul[target] = ult.get(target, 0)
            ult[target] = turn
        else:
            # Calculate the difference
            num = ult[target] - second_last_idx
            target = num
            
            if target not in ult:
                penul[target] = 0
                ult[target] = turn
            else:
                penul[target] = ult[target]
                ult[target] = turn
        
        turn += 1
    
    return target

ans_p1 = create_number_sequence_v2(starting_no, 2020)
print("Part 1:", ans_p1)

ans_p2 = create_number_sequence_v2(starting_no, 30000000)
print("Part 2:", ans_p2)
