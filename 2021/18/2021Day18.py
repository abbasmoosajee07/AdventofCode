# Advent of Code - Day 18, Year 2021
# Solution Started: Nov 25, 2024
# Puzzle Link: https://adventofcode.com/2021/day/18
# Solution by: [abbasmoosajee07]
# Brief: [Snailfish]

#!/usr/bin/env python3

import os, re, copy, itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')

def add(data):
    """Adds two snailfish numbers."""
    if " + " in data:
        left, right = data.split(" + ")
        data = f"[{left},{right}]"
    return data


def explode(data):
    """Performs the explode operation on snailfish numbers."""
    offset = 0
    for pair in re.findall(r"\[\d+,\d+\]", data):
        match = re.search(re.escape(pair), data[offset:])
        if not match:
            continue
        left_brackets = data[:match.start() + offset].count("[")
        right_brackets = data[:match.start() + offset].count("]")
        if left_brackets - right_brackets >= 4:
            x, y = map(int, pair[1:-1].split(","))
            # Split the string into two parts around the pair
            left_part = data[:match.start() + offset][::-1]
            right_part = data[match.end() + offset:]
            # Look for the nearest number to the left
            left_match = re.search(r"\d+", left_part)
            if left_match:
                left_number = int(left_part[left_match.start():left_match.end()][::-1])
                new_left_number = left_number + x
                left_part = (f"{left_part[:left_match.start()]}{str(new_left_number)[::-1]}"
                                f"{left_part[left_match.end():]}")
            # Look for the nearest number to the right
            right_match = re.search(r"\d+", right_part)
            if right_match:
                right_number = int(right_part[right_match.start():right_match.end()])
                new_right_number = right_number + y
                right_part = (f"{right_part[:right_match.start()]}{new_right_number}"
                                f"{right_part[right_match.end():]}")
            data = f"{left_part[::-1]}0{right_part}"
            break
        else:
            offset += match.end()
    return data


def split(data):
    """Performs the split operation on snailfish numbers."""
    match = re.search(r"\d\d", data)  # Find a number >= 10
    if match:
        left_part = data[:match.start()]
        right_part = data[match.end():]
        number = int(match.group())
        left_split = number // 2
        right_split = -(-number // 2)  # Ceiling division
        data = f"{left_part}[{left_split},{right_split}]{right_part}"
    return data


def reduce(data):
    """Reduces a snailfish number until stable."""
    while True:
        exploded = explode(data)
        if exploded != data:
            data = exploded
            continue
        split_data = split(data)
        if split_data != data:
            data = split_data
            continue
        break
    return data


def magnitude(data):
    """Calculates the magnitude of a snailfish number."""
    while re.search(r"\[\d+,\d+\]", data):
        for pair in re.findall(r"\[\d+,\d+\]", data):
            match = re.search(re.escape(pair), data)
            left, right = map(int, pair[1:-1].split(","))
            mag = left * 3 + right * 2
            data = f"{data[:match.start()]}{mag}{data[match.end():]}"
    return int(data)


# PART 1

# Add all snailfish numbers together
current_sum = input_data[0]
for line in input_data[1:]:
    current_sum = reduce(add(f"{current_sum} + {line}"))
part1_result = magnitude(current_sum)
print(f"Part 1: {part1_result}")

# PART 2
magnitudes = set()
for left, right in itertools.permutations(input_data, 2):
    sum_result = reduce(add(f"{left} + {right}"))
    magnitudes.add(magnitude(sum_result))
part2_result = max(magnitudes)
print(f"Part 2: {part2_result}")
