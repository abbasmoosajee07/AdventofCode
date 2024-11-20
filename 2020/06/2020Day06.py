# Advent of Code - Day 6, Year 2020
# Solution Started: Nov 20, 2024
# Puzzle Link: https://adventofcode.com/2020/day/6
# Solution by: [abbasmoosajee07]
# Brief: [Counting strings]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def count_answers(answer_list):
    count_p1 = 0
    count_p2 = 0

    for group in answer_list:
        q_count = Counter(group)
        # Part 1 Count
        if '\n' in q_count: # Remove '\n' key
            del q_count['\n']
        count_p1 += len(q_count)

        # Part 2: Count questions where everyone answered "yes"
        people = group.split('\n')
        if people:  # Ensure the group isn't empty
            common_answers = set(people[0])  # Start with the first person's answers
            for person in people[1:]:  # Intersect with subsequent people
                common_answers &= set(person)
            count_p2 += len(common_answers)
    return count_p1, count_p2

ans_p1, ans_p2 = count_answers(input_data)
print("Part 1", ans_p1)
print("Part 2", ans_p2)