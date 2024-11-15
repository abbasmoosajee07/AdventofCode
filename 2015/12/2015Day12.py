# Advent of Code - Day 12, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/12
# Solution by: [abbasmoosajee07]
# Brief: [Reading JSON data]

import os
import json
import numpy as np

D12_file = 'Day12_input.txt'
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Open and read the JSON file
with open(D12_file_path, 'r') as file:
    data = json.load(file)

def sum_numbers(data, ignore_color=False, color = "none"):
    # Initialize sum
    total_sum = 0
    
    # Check the type of the data
    if isinstance(data, dict):  # If it's a dictionary
        # If we are ignoring color, use color input in function
        if ignore_color and color in data.values():
            return 0  # Ignore this object and its children
        
        for value in data.values():
            total_sum += sum_numbers(value, ignore_color, color)  # Recursively sum values
    
    elif isinstance(data, list):  # If it's a list
        for item in data:
            total_sum += sum_numbers(item, ignore_color, color)  # Recursively sum items

    elif isinstance(data, int) or isinstance(data, float):  # If it's a number
        total_sum += data  # Add the number to the sum
    
    return total_sum

# Calculate the sum of all numbers
result_all = sum_numbers(data)
print("Sum of all numbers:", result_all)

# Calculate the sum of all numbers, ignoring any color as defined in remove_color
remove_color = "red"
result_sans_red = sum_numbers(data, ignore_color=True, color = remove_color)
print(f"Sum of all numbers, ignoring {remove_color}: {result_sans_red}")
