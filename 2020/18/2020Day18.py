# Advent of Code - Day 18, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/18
# Solution by: [abbasmoosajee07]
# Brief: [Changing the Rules of Math]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator as op

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Read and sort input data into a grid
with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_data = [r.replace(" ", "") for r in input_data]

# Operators with corresponding functions from the operator module
operators = {"*": op.mul, "+": op.add}

def evaluate(data, prec):
    """Evaluate the expression using given precedence rules."""
    operate = None  # No operator yet
    acc = 0         # Accumulator for the result
    while (char := next(data, ")")) != ")":
        if char in operators:
            operate = operators[char]
            # Check precedence: "L" means left to right, and precedence order decides precedence behavior
            if prec[-1] in (char, "L"):
                return operate(acc, evaluate(data, prec))  # Evaluate recursively if the operator's precedence matches
            continue
        # Handle the value (recursively evaluate if it's a subexpression)
        value = evaluate(data, prec) if char == "(" else int(char)
        # If no operator, just set the accumulator to the value
        acc = value if operate is None else operate(acc, value)
    return acc


# Precedence Options
precedences = ("LR", "+*", "*+" , "RL")

ans_p1 = sum(evaluate(iter(d), 'LR') for d in input_data)
print("Part 1:", ans_p1)

ans_p2 = sum(evaluate(iter(d), '+*') for d in input_data)
print("Part 2:", ans_p2)
