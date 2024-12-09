"""Advent of Code - Day 16, Year 2022
Solution Started: Dec 3, 2024
Puzzle Link: https://adventofcode.com/2022/day/16
Solution by: abbasmoosajee07
Brief: [Pipe Networks and Valves]
"""

#!/usr/bin/env python3

import os, re, copy, sys, functools
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n')


def parse_input(input_list):
    pipe_dict = {}
    pattern = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    for line in input_list:
        match = re.search(pattern, line)
        if match:
            valve = match.group(1)
            flow = int(match.group(2))
            leads_to = match.group(3).split(", ")
            pipe_dict[valve] = {'flow': flow, 'leads_to': leads_to}
    return pipe_dict


@functools.cache
def release_max_pressure(opened, mins_remaining, curr_valve_id, with_elephant=False):
    if mins_remaining <= 0:
        # If we have an elephant, start over with a fresh cycle
        if with_elephant:
            return release_max_pressure(opened, 26, "AA", with_elephant=False)
        else:
            return 0

    pressure_relief = 0
    current_valve = valve_dict[curr_valve_id]
    leads_to = current_valve["leads_to"]
    flow_rate = current_valve["flow"]

    # Skip valves with no flow rate
    if flow_rate == 0 and curr_valve_id not in opened:
        # We will not open this valve, so skip further exploration
        return max(pressure_relief, max(
            release_max_pressure(opened, mins_remaining - 1, neighbor, with_elephant) for neighbor in leads_to
        ))

    # Explore neighbors
    for neighbor in leads_to:
        pressure_relief = max(
            pressure_relief,
            release_max_pressure(opened, mins_remaining - 1, neighbor, with_elephant)
        )

    # Open the valve if not already opened and has a flow rate > 0
    if curr_valve_id not in opened and flow_rate > 0:
        new_opened = frozenset(opened | {curr_valve_id})
        total_released = (mins_remaining - 1) * flow_rate
        most_relief = 0

        for neighbor in leads_to:
            most_relief = max(
                most_relief,
                total_released + release_max_pressure(new_opened, mins_remaining - 2, neighbor, with_elephant)
            )

        pressure_relief = max(pressure_relief, most_relief)

    return pressure_relief


# valve_dict = parse_input(input_data)
# ans_p1 = release_max_pressure(frozenset(), 30, 'AA')
# print(f"Part 1: {ans_p1}")

# ans_p2 = release_max_pressure(frozenset(), 26, 'AA', True)
# print(f"Part 2: {ans_p2}")

#!/usr/bin/env python3

import os, re, functools
import numpy as np

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n')


def parse_input(input_list):
    pipe_dict = {}
    valve_names = []
    pattern = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    for line in input_list:
        match = re.search(pattern, line)
        if match:
            valve = match.group(1)
            flow = int(match.group(2))
            leads_to = match.group(3).split(", ")
            pipe_dict[valve] = {'flow': flow, 'leads_to': leads_to}
            valve_names.append(valve)
    return pipe_dict, valve_names


@functools.cache
def release_max_pressure(opened_mask, mins_remaining, curr_valve_id, with_elephant=False):
    if mins_remaining <= 0:
        # If we have an elephant, start over with a fresh cycle
        if with_elephant:
            return release_max_pressure(opened_mask, 26, "AA", with_elephant=False)
        else:
            return 0

    pressure_relief = 0
    current_valve = valve_dict[curr_valve_id]
    leads_to = current_valve["leads_to"]
    flow_rate = current_valve["flow"]

    # Skip valves with no flow rate
    if flow_rate == 0 and (opened_mask & (1 << valve_index_map[curr_valve_id])) == 0:
        # We will not open this valve, so skip further exploration
        return max(pressure_relief, max(
            release_max_pressure(opened_mask, mins_remaining - 1, neighbor, with_elephant)
            for neighbor in leads_to
        ))

    # Explore neighbors
    for neighbor in leads_to:
        pressure_relief = max(
            pressure_relief,
            release_max_pressure(opened_mask, mins_remaining - 1, neighbor, with_elephant)
        )

    # Open the valve if not already opened and has a flow rate > 0
    if (opened_mask & (1 << valve_index_map[curr_valve_id])) == 0 and flow_rate > 0:
        new_opened_mask = opened_mask | (1 << valve_index_map[curr_valve_id])
        total_released = (mins_remaining - 1) * flow_rate
        most_relief = 0

        for neighbor in leads_to:
            most_relief = max(
                most_relief,
                total_released + release_max_pressure(new_opened_mask, mins_remaining - 2, neighbor, with_elephant)
            )

        pressure_relief = max(pressure_relief, most_relief)

    return pressure_relief


# Parse input and create a mapping of valve names to indices for bitmasking
valve_dict, valve_names = parse_input(input_data)
valve_index_map = {valve_names[i]: i for i in range(len(valve_names))}

# Compute max pressure release
ans_p1 = release_max_pressure(0, 30, 'AA')
print(f"Part 1: {ans_p1}")

ans_p2 = release_max_pressure(0, 26, 'AA', True)
print(f"Part 2: {ans_p2}")
