"""Advent of Code - Day 13, Year 2024
Solution Started: Dec 13, 2024
Puzzle Link: https://adventofcode.com/2024/day/13
Solution by: abbasmoosajee07
Brief: [Solving Simultaneous Equations]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start = time.time()
# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read and sort input data into a grid
with open(D13_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_input(input_list):
    claw_machine = {}
    for no, machine in enumerate(input_list):
        match = re.findall(r'\d+', machine)
        a_x, a_y, b_x, b_y, prize_x, prize_y = map(int, match)
        # claw_machine[no] = {'A':{'X':a_x, 'Y':a_y},
        #                     'B': {'X': b_x, 'Y': b_y},
        #                     'Prize':{'X':prize_x, 'Y':prize_y}}
        claw_machine[no + 1] = {'A_x':a_x, 'A_y':a_y,
                            'B_x':b_x, 'B_y':b_y,
                            'Prize_x':prize_x, 'Prize_y':prize_y}
    return claw_machine

def solve_equations(prize_x, prize_y, a_x, a_y, b_x, b_y):

    # Calculate the number of times to press button B (press_B)
    numerator_b = prize_y - (prize_x * a_y / a_x)
    denominator_b = b_y - (b_x * a_y / a_x)

    if denominator_b == 0:  # Prevent division by zero
        return 0, 0, 0

    press_b = numerator_b / denominator_b

    # Calculate the number of times to press button A (press_A)
    press_a = (prize_x - press_b * b_x) / a_x

    # Convert to integers for verification
    int_a = round(press_a, 0)
    int_b = round(press_b, 0)

    # Verify if the calculated presses match the prize coordinates
    if (int_a * a_x + int_b * b_x == prize_x) and (int_a * a_y + int_b * b_y == prize_y):
        tokens = (3 * int_a) + int_b
        return int_a, int_b, int(tokens)

    return 0, 0, 0

def calc_min_tokens(claw_machines, prize_shift = 0):
    total_tokens = 0
    for machine_no in claw_machines.keys():
        test_machine = claw_machines[machine_no]
        # Example values
        Prize_x = test_machine['Prize_x'] + prize_shift
        Prize_y = test_machine['Prize_y'] + prize_shift
        A_x = test_machine['A_x']
        A_y = test_machine['A_y']
        B_x = test_machine['B_x']
        B_y = test_machine['B_y']

        press_A, press_B, tokens = solve_equations(Prize_x, Prize_y, A_x, A_y, B_x, B_y)
        total_tokens += tokens
    return total_tokens

claw_dict = parse_input(input_data)
ans_p1 = calc_min_tokens(claw_dict)
print("Part 1:", ans_p1)

ans_p2 = calc_min_tokens(claw_dict, prize_shift=10_000_000_000_000)
print("Part 2:", ans_p2)
print(time.time() - start)