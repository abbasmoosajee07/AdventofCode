"""Advent of Code - Day 19, Year 2023
Solution Started: Jan 8, 2025
Puzzle Link: https://adventofcode.com/2023/day/19
Solution by: abbasmoosajee07
Brief: [Validating Parts in Workflows]
"""

#!/usr/bin/env python3

import os, re, copy, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import sympify

# Load the input data from the specified file path
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_input(input_list: list) -> tuple[dict, list]:
    workflow_dict = {}
    for flow in input_list[0].split('\n'):
        workflow, rules = flow.split('{')
        workflow_dict[workflow] = rules.strip('}').split(',')

    parts_list = []
    for parts in input_list[1].split('\n'):
        parts_dict = {}
        strip_parts = parts.strip('{}').split(',')
        for specific_part in strip_parts:
            name, value = specific_part.split('=')
            parts_dict[name] = int(value)
        parts_list.append(parts_dict)
    return workflow_dict, parts_list

def sort_parts_list(workflow_dict: dict, parts_list: list[dict]) -> int:
    """ Processes workflows and parts to calculate the total sum of accepted parts. """

    total_accepted = 0
    for part in parts_list:
        curr_workflow = 'in'  # Start at the 'in' workflow
        while curr_workflow not in ('A', 'R'):  # Loop until accepted ('A') or rejected ('R')
            rules = workflow_dict[curr_workflow]
            for rule in rules[:-1]:  # Exclude the default final state
                # Parse the rule into its components
                var, op, threshold, next_state = re.match(r'(\w+)([<>])(\d+):(\w+)', rule).groups()

                # Check the condition using the parsed operator and threshold
                if sympify(f"{part[var]} {op} {threshold}"):
                    curr_workflow = next_state
                    break
            else:
                # If no condition matched, follow the final state
                curr_workflow = rules[-1]

        # If the part is accepted, add its values to the total
        if curr_workflow == 'A':
            total_accepted += sum(part.values())

    return total_accepted

def extended_parts_list(workflow_dict: dict, max_num: int = 1000) -> int:
    """ Calculates the total possible range of accepted parts based on workflows and intervals."""
    start = ('in', (1, max_num), (1, max_num), (1, max_num), (1, max_num))
    queue = [start]
    total_accepted = 0

    while queue:
        curr_workflow, *intervals = queue.pop()
        if curr_workflow in ('A', 'R'):
            if curr_workflow == 'A':
                total_accepted += math.prod(hi - lo + 1 for lo, hi in intervals)
            continue

        rules = workflow_dict[curr_workflow]
        for rule in rules[:-1]:  # Exclude the default final state
            condition, next_workflow = rule.split(':')
            var, op, threshold = re.match(r'(\w+)([<>])(\d+)', condition).groups()
            var_idx = 'xmas'.index(var)  # Map variable to index (x=0, m=1, a=2, s=3)
            lo, hi = intervals[var_idx]

            # All passthrough, no transfer
            threshold = int(threshold)
            if (op == '>' and threshold >= hi) or (op == '<' and threshold <= lo):
                continue

            # All transfer, no passthrough
            if (op == '>' and threshold < lo) or (op == '<' and threshold > hi):
                queue.append((next_workflow, *intervals))
                break

            # Some of both
            if op == '>':
                transfer = (threshold + 1, hi)
                passthrough = (lo, threshold)
            elif op == '<':
                transfer = (lo, threshold - 1)
                passthrough = (threshold, hi)

            # Update intervals for passthrough and transfer cases
            intervals[var_idx] = passthrough
            intervals2 = intervals.copy()
            intervals2[var_idx] = transfer
            queue.append((next_workflow, *intervals2))

        else:  # If no conditions matched, transfer to the default state
            queue.append((rules[-1], *intervals))

    return total_accepted

workflow_dict, part_list = parse_input(input_data)

accepted_parts_p1 = sort_parts_list(workflow_dict, part_list)
print("Part 1:", accepted_parts_p1)

accepted_parts_p2 = extended_parts_list(workflow_dict, max_num=4000)
print("Part 2:", accepted_parts_p2)
