"""Advent of Code - Day 7, Year 2024
Solution Started: Dec 7, 2024
Puzzle Link: https://adventofcode.com/2024/day/7
Solution by: abbasmoosajee07
Brief: [Build Numbers]
"""

#!/usr/bin/env python3

import os, time
from itertools import product
start_time = time.time()
# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and parse the input
with open(D07_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input):
    num_dict = {}
    for line in input:
        target, blocks = line.split(': ')
        num_dict[int(target)] = [int(num) for num in blocks.split(' ')]
    return num_dict

def can_build_target(target, blocks, operators=['+', '*', '-', '/', '||']): 
    """
    Determines if the target can be built using the blocks in order and basic operations.
    
    Args:
        target (int): The target number.
        blocks (list): A list of numbers that must be used in order.
        operators (list): Valid set of operators ['+', '*', '-', '/', '||']
    
    Returns:
        bool: True if the target can be formed, False otherwise.
    """
    # Cache of results to avoid duplicate evaluations
    cache = {}

    def evaluate(numbers, ops):
        """
        Evaluates an expression given numbers and operators.
        """
        key = (tuple(numbers), tuple(ops))
        if key in cache:
            return cache[key]

        try:
            result = numbers[0]
            for i, op in enumerate(ops):
                if op == '+':
                    result += numbers[i + 1]
                    if result > target:  # Early pruning for addition
                        cache[key] = False
                        return False
                elif op == '*':
                    result *= numbers[i + 1]
                    if result > target and all(n > 0 for n in numbers):  # Early pruning for multiplication
                        cache[key] = False
                        return False
                elif op == '||':
                    # Concatenate the numbers and convert to integer
                    result = int(str(int(result)) + str(int(numbers[i + 1])))
                elif op == '-':
                    result -= numbers[i + 1]
                elif op == '/':
                    if numbers[i + 1] == 0:  # Avoid division by zero
                        cache[key] = False
                        return False
                    result /= numbers[i + 1]
                    if not result.is_integer():  # Avoid non-integer results
                        cache[key] = False
                        return False

            is_target = result == target
            cache[key] = is_target
            return is_target
        except ZeroDivisionError:
            return False

    # Generate all combinations of operators for the given block order
    for ops in product(operators, repeat=len(blocks) - 1):
        if evaluate(blocks, ops):  # Stop if a valid expression is found
            return True

    return False

def calibrate_machine(num_dict, operators):
    # Calculate the calibration score
    calibration = 0
    for target, blocks in num_dict.items():
        if can_build_target(target, blocks, operators):
            calibration += target
    return calibration

bridge_dict = parse_input(input_data)

# Part 1
ans_p1 = calibrate_machine(bridge_dict, operators=['+', '*'])
print("Part 1:", ans_p1)

# Part 2
ans_p2 = calibrate_machine(bridge_dict, operators=['+', '*', '||'])
print("Part 2:", ans_p2)
print("Total Time:",time.time()- start_time)
