# Advent of Code - Day 10, Year 2020
# Solution Started: Nov 20, 2024
# Puzzle Link: https://adventofcode.com/2020/day/10
# Solution by: [abbasmoosajee07]
# Brief: [Number Arrangements]

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a list of integers
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')
    num_list = [int(num) for num in input_data]
    adapter_set = set(num_list)

def find_jolt_range(num):
    """Return the set of usable adapters within the jolt range of 1, 2, and 3."""
    return {num + 1, num + 2, num + 3}

def count_arrangements(adapters):
    """Count the distinct arrangements of adapters."""
    adapters = [0] + sorted(adapters) + [max(adapters) + 3]
    ways = {0: 1}  # There's 1 way to reach the outlet (0 jolts)

    # Calculate the number of ways to reach each adapter
    for adapter in adapters[1:]:
        ways[adapter] = ways.get(adapter - 1, 0) + ways.get(adapter - 2, 0) + ways.get(adapter - 3, 0)

    return ways[adapters[-1]]

# Part 1: Calculate the difference counts (1-jolt, 2-jolt, and 3-jolt differences)
charging_joltage = 0
current_adapter = charging_joltage
remaining_adapters = set(num_list)
diff_1 = diff_2 = diff_3 = 0

while remaining_adapters:
    useable_adapters = find_jolt_range(current_adapter)
    common = useable_adapters & remaining_adapters
    selected_adapter = min(common)
    remaining_adapters.remove(selected_adapter)

    diff = selected_adapter - current_adapter
    current_adapter = selected_adapter

    if diff == 1:
        diff_1 += 1
    elif diff == 2:
        diff_2 += 1
    elif diff == 3:
        diff_3 += 1

# Add the 3-jolt difference for the built-in adapter
diff_3 += 1

# Part 1 answer: 1-jolt difference count * 3-jolt difference count
ans_p1 = diff_1 * diff_3
print(f"Part 1: {ans_p1}")

# Part 2: Count distinct arrangements of adapters
arrangements = count_arrangements(num_list)
print(f"Part 2: Distinct arrangements: {arrangements}")
