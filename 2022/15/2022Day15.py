"""Advent of Code - Day 15, Year 2022
Solution Started: Dec 2, 2024
Puzzle Link: https://adventofcode.com/2022/day/15
Solution by: abbasmoosajee07
Brief: [Sensors and Beacons Area Coverage]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Read and sort input data into a grid
with open(D15_file_path) as file:
    input_data = file.read().strip().split('\n')


def parse_input(input_list):
    sensor_beacon = []
    pattern = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    for sensor in input_list:
        match = re.search(pattern, sensor)
        sx, sy, bx, by = map(int, match.groups())
        sensor_beacon.append([(sx, sy), (bx, by)])
    return sensor_beacon

def calc_manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def get_x_range_for_row(sensor, row):
    sx, sy = sensor[0]
    bx, by = sensor[1]
    dist = calc_manhattan_distance(sx, sy, bx, by)

    # Check if the row is within the sensor's coverage area
    row_distance = abs(sy - row)
    if row_distance > dist:
        return None  # No coverage on this row

    # Calculate the horizontal range of coverage on this row
    horizontal_range = dist - row_distance
    return (sx - horizontal_range, sx + horizontal_range)

def count_unique_coverage_on_row(sensor_beacon_pairs, row):
    ranges = []
    
    # Get the range of coverage for each sensor
    for pair in sensor_beacon_pairs:
        range_for_row = get_x_range_for_row(pair, row)
        if range_for_row:
            ranges.append(range_for_row)
    
    # Sort the ranges by the starting x-coordinate
    ranges.sort()
    
    # Merge overlapping or adjacent ranges
    merged_ranges = []
    current_range = ranges[0]
    
    for r in ranges[1:]:
        if r[0] <= current_range[1] + 1:  # Ranges overlap or are adjacent
            current_range = (current_range[0], max(current_range[1], r[1]))
        else:
            merged_ranges.append(current_range)
            current_range = r
    
    # Add the last range
    merged_ranges.append(current_range)
    
    # Count the total number of covered x-coordinates, excluding beacon positions
    total_coverage = 0
    beacon_positions = set([(bx, by) for _, (bx, by) in sensor_beacon_pairs])
    
    for r in merged_ranges:
        # Count the number of x-coordinates in this range
        for x in range(r[0], r[1] + 1):
            if (x, row) not in beacon_positions:
                total_coverage += 1
    
    return total_coverage


def find_non_covered_spot(sensor_beacon_pairs, max_row=4_000):
    # Track ranges of covered x-coordinates for each row
    for row in range(max_row + 1):
        ranges = []
        
        # Get the range of coverage for each sensor
        for pair in sensor_beacon_pairs:
            range_for_row = get_x_range_for_row(pair, row)
            if range_for_row:
                ranges.append(range_for_row)
        
        # Sort the ranges by the starting x-coordinate
        ranges.sort()
        
        # Merge overlapping or adjacent ranges
        merged_ranges = []
        current_range = ranges[0]
        
        for r in ranges[1:]:
            if r[0] <= current_range[1] + 1:  # Ranges overlap or are adjacent
                current_range = (current_range[0], max(current_range[1], r[1]))
            else:
                merged_ranges.append(current_range)
                current_range = r
        
        # Add the last range
        merged_ranges.append(current_range)
        
        # After merging, check for a gap in coverage
        for r in merged_ranges:
            # If there's a gap before the start of the range, return that position
            if r[0] > 0:
                return (r[0] - 1, row)
    
    return None  # If no valid spot is found

# Example Row to check
target_row = 2000000
sensor_beacon_pairs = parse_input(input_data)

# Calculate total coverage
ans_p1 = count_unique_coverage_on_row(sensor_beacon_pairs, target_row)
print("Part 1:", ans_p1)

# Find a non-covered spot
max_row = 4_000_000
non_covered_spot = find_non_covered_spot(sensor_beacon_pairs, max_row=max_row)
print("Part 2:", (non_covered_spot[0] * max_row) + non_covered_spot[1])
