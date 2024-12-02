"""Advent of Code - Day 11, Year 2022
Solution Started: Nov 30, 2024
Puzzle Link: https://adventofcode.com/2022/day/11
Solution by: abbasmoosajee07
Brief: [Monkeys and Worry Lists]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import sympy as sp
from math import gcd
from functools import reduce

# Load the input data from the specified file path
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Read and sort input data into a grid
with open(D11_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_input(monkey_list):
    """Parses input and returns a dictionary representing each monkey's data."""
    monkey_dict = {}
    for monkey in monkey_list:
        monkey_data = monkey.split('\n')
        monkey_no = int(monkey_data[0].strip('Monkey ').strip(':'))
        starting = [int(num) for num in monkey_data[1].strip('Starting items: ').split(',')]
        _, operation = monkey_data[2].split(' = ')
        test = int(monkey_data[3].strip('Test: divisible by '))
        true = int(monkey_data[4].strip('If true: throw to monkey '))
        false = int(monkey_data[5].strip('If false: throw to monkey '))
        
        # Initialize monkey properties
        monkey_props = {
            'starting': starting,
            'op': operation,
            'test': test,
            'true': true,
            'false': false,
            'inspect': 0  # Counter for inspections
        }
        monkey_dict[monkey_no] = monkey_props
    
    return monkey_dict

def basic_monkey_turn(monkey_dict, no, modulus = None):
    """Performs a single turn for the given monkey."""
    monkey_data = monkey_dict[no]
    worry_list = monkey_data['starting']
    operation = monkey_data['op']

    for worry_level in worry_list:
        old = worry_level
        
        # Substitute 'old' into the operation and evaluate
        expr = operation.replace('old', str(old))
        result = sp.sympify(expr)
        
        # Calculate new worry level and decide which monkey to throw to
        new_worry = result // 3
        if new_worry % monkey_data['test'] == 0:
            throw = monkey_data['true']
        else:
            throw = monkey_data['false']
        
        # Add new worry level to the target monkey's starting list
        monkey_dict[throw]['starting'].append(new_worry)
        
        # Increment the inspection counter
        monkey_dict[no]['inspect'] += 1

    # Clear the current monkey's 'starting' list
    monkey_data['starting'] = []

def busiest_monkeys(final_dict):
    inspect_counts = []
    for key in sorted(final_dict.keys()):
        counts = final_dict[key]['inspect']
        inspect_counts.append(counts)
    sorted_inspect_counts = sorted(inspect_counts)
    busy_score = sorted_inspect_counts[-1] * sorted_inspect_counts[-2]
    return busy_score

def lcm(a, b):
    """Calculate the Least Common Multiple (LCM) of two numbers."""
    return abs(a * b) // gcd(a, b)

def compute_lcm_of_tests(monkey_dict):
    """Compute the LCM of all test divisors."""
    test_values = [monkey_dict[key]['test'] for key in monkey_dict]
    return reduce(lcm, test_values)

def modular_monkey_turn(monkey_dict, no, modulus):
    """Perform a single turn for the given monkey, using modular arithmetic."""
    monkey_data = monkey_dict[no]
    worry_list = monkey_data['starting']
    operation = monkey_data['op']
    
    for worry_level in worry_list:
        old = worry_level
        
        # Substitute 'old' into the operation and evaluate
        expr = operation.replace('old', str(old))
        result = sp.sympify(expr)
        
        # Apply modular arithmetic to limit worry level growth
        new_worry = (result % modulus)
        
        # Determine which monkey to throw to based on divisibility test
        if new_worry % monkey_data['test'] == 0:
            throw = monkey_data['true']
        else:
            throw = monkey_data['false']
        
        # Add the new worry level to the target monkey's starting list
        monkey_dict[throw]['starting'].append(new_worry)
        
        # Increment the inspection counter
        monkey_dict[no]['inspect'] += 1

    # Clear the current monkey's 'starting' list
    monkey_data['starting'] = []

def play_rounds(monkey_dict, function, total_rounds, modulus = None):
    """Simulates multiple rounds of monkey operations."""
    for round in range(total_rounds):
        # print(round)
        for key in sorted(monkey_dict.keys()):  # Ensure deterministic order
            modulus = compute_lcm_of_tests(monkey_dict)
            function(monkey_dict, key, modulus)
    busy_score = busiest_monkeys(monkey_dict)
    return monkey_dict, busy_score

monkey_dict = parse_input(input_data)
final_dict_p1, ans_p1 = play_rounds(monkey_dict, basic_monkey_turn, total_rounds=20)
print("Part 1:", ans_p1)

monkey_dict = parse_input(input_data)
modulus = compute_lcm_of_tests(monkey_dict)
final_dict_p2, ans_p2 = play_rounds(monkey_dict,
        modular_monkey_turn, total_rounds=10000, modulus=modulus)
print(f"Part 2: {ans_p2}")
