"""Advent of Code - Day 21, Year 2022
Solution Started: Dec 10, 2024
Puzzle Link: https://adventofcode.com/2022/day/21
Solution by: abbasmoosajee07
Brief: []
"""

#!/usr/bin/env python3

import os, re, copy, time, ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split('\n')
    instruction_dict = {line.split(': ')[0]: line.split(': ')[1] for line in input_data}

def parse_expression(expr):
    """Recursively parse a nested list into a sympy expression."""
    if isinstance(expr, str):
        if expr == "your_input":
            return symbols("your_input")  # Treat 'your_input' as a variable
        return int(expr)  # Convert numeric strings to integers
    
    if isinstance(expr, list):
        left = parse_expression(expr[0])
        operator = expr[1]
        right = parse_expression(expr[2])
        
        # Build the sympy expression based on the operator
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left / right
        elif operator == '=':
            return Eq(left, right)
        else:
            raise ValueError(f"Unsupported operator: {operator}")

def find_monkey_call(instructions, start = 'root'):
    equation = instructions[start].split()
    # print(start, equation)
    if len(equation) == 1:
        return equation[0]
    elif len(equation) >= 2:
        new_equation = []
        for variable in equation:
            if variable not in ['+','-','*','/', '=']:
                next_variable = find_monkey_call(instructions, variable)
                new_equation.append(next_variable)
            else:
                new_equation.append(variable)
        return new_equation

def match_monkey_call(instructions: dict):
    root_instruction = re.sub(r'[+\-*/^]', '=', instructions['root'])
    instructions['root'] = root_instruction
    instructions['humn'] = 'your_input'
    equation = find_monkey_call(instructions)
    # Parse the equation into a sympy Eq object
    lhs = parse_expression(equation[0])  # Left-hand side of the equation
    rhs = parse_expression(equation[2])  # Right-hand side of the equation
    eq = Eq(lhs, rhs)  # Create the equation
    
    # Solve for 'your_input'
    your_input = symbols("your_input")
    solution = solve(eq, your_input)
    return round(solution[0])

eq_p1 = find_monkey_call(instruction_dict)
ans_p1 = parse_expression(eq_p1)
print("Part 1:", round(ans_p1))

ans_p2 = match_monkey_call(instruction_dict)
print("Part 2:", ans_p2)
