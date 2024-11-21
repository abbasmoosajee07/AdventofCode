# Advent of Code - Day 14, Year 2020
# Solution Started: Nov 21, 2024
# Puzzle Link: https://adventofcode.com/2020/day/14
# Solution by: [abbasmoosajee07]
# Brief: [Bit Memory]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path) as file:
    input_data = file.read().strip().split('\n')

mask_regex = re.compile(r"^mask = ([01X]{36})$")
mem_regex = re.compile(r"^mem\[(\d+)\] = (\d+)$")

# --- Part One ---
memory = {}
zero_mask = one_mask = 0

for line in input_data:
    mask_match = mask_regex.match(line)
    mem_match = mem_regex.match(line)

    if mask_match:
        mask = mask_match.group(1)
        zero_mask = int(mask.replace("X", "1"), 2)
        one_mask = int(mask.replace("X", "0"), 2)
    elif mem_match:
        address = int(mem_match.group(1))
        value = int(mem_match.group(2))
        memory[address] = (value & zero_mask) | one_mask
    else:
        raise ValueError(f"Unexpected line: {line}")

print("Part 1:",sum(memory.values()))

# --- Part Two ---
memory = {}
zero_mask = one_mask = 0
floating_bits = []

for line in input_data:
    mask_match = mask_regex.match(line)
    mem_match = mem_regex.match(line)

    if mask_match:
        mask = mask_match.group(1)
        zero_mask = int(mask.replace("X", "1"), 2)
        one_mask = int(mask.replace("X", "0"), 2)
        floating_bits = [35 - i for i, char in enumerate(mask) if char == 'X']
    elif mem_match:
        address = int(mem_match.group(1))
        value = int(mem_match.group(2))

        for counter in range(1 << len(floating_bits)):
            new_address = (address & ~zero_mask) | one_mask
            for i, bit_position in enumerate(floating_bits):
                bit = (counter >> i) & 1
                new_address |= bit << bit_position
            memory[new_address] = value
    else:
        raise ValueError(f"Unexpected line: {line}")

print("Part 2:",sum(memory.values()))

