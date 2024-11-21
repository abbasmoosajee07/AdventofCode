# Advent of Code - Day 9, Year 2020
# Solution Started: Nov 20, 2024
# Puzzle Link: https://adventofcode.com/2020/day/9
# Solution by: [abbasmoosajee07]
# Brief: [Num Sum w/ preambles]

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
    input_data = file.read().strip().split('\n')
    num_list = [int(num) for num in input_data]

preamble = 25

def can_sum_set(nums, target):
    seen = set()  # Set to store numbers we've seen

    for num in nums:
        complement = target - num
        if complement in seen:
            return True  # Found two numbers that add to target
        seen.add(num)

    return False  # No such pair exists

for pos in range(preamble,len(num_list)):
    preamble_nums = num_list[pos-preamble:pos]
    valid_cond = can_sum_set(preamble_nums, num_list[pos])
    if not valid_cond:
        target = num_list[pos]
        break

print("Part 1:", target)

def find_contiguous_sum(nums, target):
    """
    Find the contiguous subsequence that sums to the target.
    Returns the smallest and largest numbers in that subsequence.
    """
    start, current_sum = 0, 0

    for end in range(len(nums)):
        current_sum += nums[end]

        # Shrink the window from the start if the sum exceeds the target
        while current_sum > target:
            current_sum -= nums[start]
            start += 1

        # If the sum matches the target, return the result
        if current_sum == target:
            contiguous_range = nums[start:end + 1]
            return min(contiguous_range) + max(contiguous_range)

    return None  # No valid range found
min_max = find_contiguous_sum(num_list, target)
print("Part 1:", min_max)
