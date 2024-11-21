# Advent of Code - Day 13, Year 2020
# Solution Started: Nov 21, 2024
# Puzzle Link: https://adventofcode.com/2020/day/13
# Solution by: [abbasmoosajee07]
# Brief: [Bus Timetable]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read and sort input data into a grid
with open(D13_file_path) as file:
    input_data = file.read().strip().split('\n')
    timestamp = int(input_data[0])
    bus_id = [bus for bus in input_data[1].split(',')]

def select_ideal_bus(timestamp, bus_id):
    active_bus = [int(active) for active in bus_id if active != 'x']
    depart_time = float('inf')
    for bus in active_bus:
        closest_dep = ((timestamp // bus) * bus) + bus
        if closest_dep < depart_time:
            depart_time = closest_dep
            bus_selected =  bus
    return (depart_time - timestamp) * bus_selected

ans_p1 = select_ideal_bus(timestamp, bus_id)
print("Part 1:", ans_p1)

def find_earliest_timestamp(bus_ids):
    # Initialize the timestamp and the step size
    timestamp = 0
    step_size = 1  # This represents the step size that increments as we find the solution.

    # Iterate over the bus IDs and their offsets
    for offset, bus in enumerate(bus_ids):
        if bus == 'x':
            continue
        bus_id = int(bus)
        # We are looking for a timestamp that satisfies: timestamp + offset ≡ 0 (mod bus_id)
        # This translates to finding the smallest timestamp `timestamp` such that:
        # timestamp ≡ -offset (mod bus_id)
        
        # Find the current timestamp that satisfies the condition using the step size
        while (timestamp + offset) % bus_id != 0:
            timestamp += step_size
        
        # After finding a valid timestamp, increment the step_size by bus_id to make sure
        # the next condition holds.
        step_size *= bus_id
    
    return timestamp

# Process the bus IDs with offsets
bus_ids = input_data[1].split(',')
ans_p2 = find_earliest_timestamp(bus_ids)

print("Part 2:", ans_p2)
