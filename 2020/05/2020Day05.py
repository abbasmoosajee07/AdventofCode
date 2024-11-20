# Advent of Code - Day 5, Year 2020
# Solution Started: Nov 20, 2024
# Puzzle Link: https://adventofcode.com/2020/day/5
# Solution by: [abbasmoosajee07]
# Brief: [Plane Seating Charts]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

# Read and sort input data into a grid
with open(D05_file_path) as file:
    input_data = file.read().strip().split('\n')
    seat_list = [list(seat) for seat in input_data]

def split_list(list, dir):
    mid = len(list) // 2  # Find the midpoint
    front = list[:mid]
    back = list[mid:]
    if dir in ['F', 'L']:
        remaining = front
    elif dir in ['B', 'R']:
        remaining = back
    return remaining

def find_seat_id(seat, plane_size):
    # Find row seat is in
    rows_rem = list(range(0, plane_size[0]))
    cols_rem = list(range(0, plane_size[1]))

    for dir in seat[0:7]:
        rows_rem = split_list(rows_rem, dir)

    for dir in seat[7:]:
        cols_rem = split_list(cols_rem, dir)
    seat_coord = (rows_rem[0], cols_rem[0])
    seat_id = (rows_rem[0] * 8) + cols_rem[0]
    return seat_coord, seat_id

def decode_seats(seat_list, plane_size):
    seat_props = []
    max_id = 0
    min_id = float('Inf')
    for seat in seat_list:
        coord, id = find_seat_id(seat, plane_size)
        max_id = max(id, max_id)
        min_id = min(id, min_id)
        seat_props.append([seat, coord, id])
    return seat_props, max_id

plane_size = [128, 8]
seat_props, ans_p1 = decode_seats(seat_list, plane_size)
print(f"Part 1: {ans_p1}")

plane_map = np.zeros((plane_size[0],plane_size[1]))

for seat in seat_props:
    coords = seat[1]
    id = seat[2]
    plane_map[coords] = id

# Flatten the plane_map to get all IDs and remove zeros (empty seats)
existing_ids = plane_map[plane_map > 0].flatten()

# Find the minimum and maximum seat IDs
min_id = int(existing_ids.min())
max_id = int(existing_ids.max())

# Calculate the sum of the full range of IDs
expected_sum = sum(range(min_id, max_id + 1))

# Calculate the actual sum of seat IDs
actual_sum = int(existing_ids.sum())

# The missing seat ID
missing_seat_id = expected_sum - actual_sum

print("Part 2:", missing_seat_id)