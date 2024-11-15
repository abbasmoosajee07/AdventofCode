# Advent of Code - Day 25, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/25
# Solution by: [abbasmoosajee07]
# Brief: [Final Day Puzzle]

import re, os

def get_next_coordinates(row: int, col: int):
    """Compute the next row and column in the sequence based on current row and column."""
    return (col + 1, 1) if row == 1 else (row - 1, col + 1)

def compute_next_code(current_code: int):
    """Generate the next code using the modular arithmetic provided."""
    return (current_code * 252533) % 33554393

def next_step(row: int, col: int, current_code: int):
    """Calculate the next row, column, and code."""
    next_row, next_col = get_next_coordinates(row, col)
    next_code = compute_next_code(current_code)
    return next_row, next_col, next_code


D25_file = 'Day25_input.txt'
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

with open(D25_file_path) as file:
    input_string = file.read()

# Initialize variables
code, row, col = 27995004, 6, 6

# Use regex to extract numbers
numbers = re.findall(r'\d+', input_string)

# Convert extracted numbers to integers
target_row, target_column = map(int, numbers)

# Continue until the target coordinates are reached
while (row, col) != (target_row, target_column): # Test Coordinates
    row, col, code = next_step(row, col, code)

print(f"The input of the puzzle: {code}")