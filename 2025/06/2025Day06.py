"""Advent of Code - Day 6, Year 2025
Solution Started: December 6, 2025
Puzzle Link: https://adventofcode.com/2025/day/6
Solution by: Abbas Moosajee
Brief: [Trash Compactor]"""

#!/usr/bin/env python3
from pathlib import Path
from math import prod
from collections import defaultdict
# Load input file
input_file = "Day06_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def traditional_math(homework_sheet):
    sheet_grid = [row.split() for row in homework_sheet]
    all_problems = [[row[i] for row in sheet_grid] for i in range(len(sheet_grid[0]))]
    total_sum = 0
    for problem in all_problems:
        problem_ints = list(map(int, problem[:-1]))
        problem_ans = 0
        if problem[-1] == '*':
            problem_ans = prod(problem_ints)
        elif problem[-1] == '+':
            problem_ans = sum(problem_ints)
        total_sum += problem_ans
    return total_sum

def cephalopod_math(homework_sheet):

    if not homework_sheet:
        return 0
    
    # Transpose the data to work with columns instead of rows
    # Find the maximum row length
    max_len = max(len(row) for row in homework_sheet)
    
    # Pad rows to ensure they're all the same length
    padded_sheet = [row + " " * (max_len - len(row)) for row in homework_sheet]
    
    total_sum = 0
    current_problem = None
    operation = None
    
    # Process each column
    for col_idx in range(max_len):
        # Get the column values
        column = [row[col_idx] for row in padded_sheet]
        
        # Check if this is a separator (all spaces in column)
        if all(cell == " " for cell in column):
            if current_problem is not None:
                total_sum += current_problem
                current_problem = None
                operation = None
            continue
        
        # Parse the current column
        try:
            # Extract digits and operator
            digits = [cell for cell in column if cell.isdigit()]
            operators = [cell for cell in column if cell in "+*-/"]
            
            if digits:
                # Combine digits to form a number
                number = int("".join(digits))
                
                if current_problem is None:
                    current_problem = number
                elif operation == "+":
                    current_problem += number
                elif operation == "*":
                    current_problem *= number
                else:
                    # No operation specified yet, treat as new problem
                    current_problem = number
            
            if operators:
                # Set the operation for next number
                operation = operators[0] if operators else None
                
        except (ValueError, IndexError):
            # Skip invalid columns
            continue
    
    # Add the last problem if exists
    if current_problem is not None:
        total_sum += current_problem
    
    return total_sum

print("AOC Day 06, P1:", traditional_math(data))
print("AOC Day 06, P2:", cephalopod_math(data))