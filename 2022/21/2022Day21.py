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
import networkx as nx
start_time = time.time()

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split('\n')
    instruction_dict = {line.split(': ')[0]: line.split(': ')[1] for line in input_data}

def evaluate_expression(expr):
    # Base case: if the expression is a single number (string), return it as a number
    if isinstance(expr, str):
        return int(expr)
    if isinstance(expr, int):
        return expr

    # Recursive case: if the expression is a list
    if isinstance(expr, list):
        # The structure of the list is [left_operand, operator, right_operand]
        left = evaluate_expression(expr[0])  # Evaluate the left operand
        operator = expr[1]  # The operator as a string
        right = evaluate_expression(expr[2])  # Evaluate the right operand

        # Perform the operation based on the operator
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left // right  # Integer division for simplicity
        elif operator == '=':
            if left == right:
                return True
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

eq_p1 = find_monkey_call(instruction_dict)
ans_p1 = evaluate_expression(eq_p1)
print("Part 1:", (ans_p1))

human_val = 301
test_input = ['root: pppw = sjmn',
    'dbpl: 5',
    'cczh: sllz + lgvd',
    'zczc: 2',
    'ptdq: humn - dvpt',
    'dvpt: 3',
    'lfqf: 4',
    f'humn: {human_val}',
    'ljgn: 2',
    'sjmn: drzm * dbpl',
    'sllz: 4',
    'pppw: cczh / lfqf',
    'lgvd: ljgn * ptdq',
    'drzm: hmdt - zczc',
    'hmdt: 32'
]
instruction_dict1 = {line.split(': ')[0]: line.split(': ')[1] for line in test_input}
eq_p2 = find_monkey_call(instruction_dict1)
ans_p2= evaluate_expression(eq_p2)
print("Part 2:", (ans_p2))
print("Total Time", time.time()-start_time)
