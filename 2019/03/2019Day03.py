# Advent of Code - Day 3, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Tracking Wires]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D03_file)

# Read and sort input data into a grid
with open(D03_file_path) as file:
    input_data = file.read().strip().split('\n')

def split_letters_numbers(string):
    letters = ''.join([char for char in string if char.isalpha()])
    numbers = ''.join([char for char in string if char.isdigit()])
    return letters, int(numbers)

def track_wire_path(movement_list, start):
    """Track the path of a wire and return a list of visited points with the number of steps"""
    wire_path = []
    current_position = start
    steps = 0
    wire_path.append((current_position, steps))  # Add the start point with 0 steps
    
    for movement in movement_list:
        dir, mag = split_letters_numbers(movement)
        if dir == 'U':
            move = complex(0, mag)  # Move upwards
        elif dir == 'D':
            move = complex(0, -mag)  # Move downwards
        elif dir == 'R':
            move = complex(mag, 0)  # Move right
        elif dir == 'L':
            move = complex(-mag, 0)  # Move left
        
        # Move step by step and record the number of steps taken
        for _ in range(mag):
            current_position += move / mag  # Move incrementally (step by step)
            steps += 1
            wire_path.append((current_position, steps))  # Record each position with the step count

    wire_dict = {pos: steps for pos, steps in wire_path}

    return wire_dict

def fewest_steps_to_intersection(wire_1, wire_2, start):

    # Find intersections (points visited by both wires)
    intersection_list = set(wire_1.keys()) & set(wire_2.keys())

    # Remove the start point from the intersection set (we don't want to count it)
    intersection_list.discard(start)

    # Find the fewest steps to any intersection
    min_steps = float('inf')  # Initialize with a large number
    for intersection in intersection_list:
        wire1_steps = wire_1[intersection]
        wire2_steps = wire_2[intersection]
        total_steps = wire1_steps + wire2_steps
        min_steps = min(min_steps, total_steps)

    return min_steps

def closest_intersection(wire_1, wire_2, start):
    """Find the closest intersection by calculating Manhattan distance"""

    # Find intersections (points visited by both wires)
    intersections = set(wire_1.keys()) & set(wire_2.keys())

    # Remove the start point from the intersection set (we don't want to count it)
    intersections.discard(start)

    # Find the Manhattan distance of the closest intersection
    closest_dist = float('inf')  # Initialize with a large number
    for intersection in intersections:
        dist = abs(intersection.real) + abs(intersection.imag)  # Manhattan distance
        if dist < closest_dist:
            closest_dist = dist

    return closest_dist


start = complex(0, 0)  # Starting point at (0x, 0y)
wire_1 = input_data[0].split(',')
wire_2 = input_data[1].split(',')

# Track the paths of both wires
wire_1_dict = track_wire_path(wire_1, start)
wire_2_dict = track_wire_path(wire_2, start)

# Find the closest intersection
closest_dist = closest_intersection(wire_1_dict, wire_2_dict, start)
print(f"Part 1: {int(closest_dist)}")

# Find the fewest steps to intersection
fewest_steps = fewest_steps_to_intersection(wire_1_dict, wire_2_dict, start)
print(f"Part 2: {fewest_steps}")