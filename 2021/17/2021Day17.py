# Advent of Code - Day 17, Year 2021
# Solution Started: Nov 25, 2024
# Puzzle Link: https://adventofcode.com/2021/day/17
# Solution by: [abbasmoosajee07]
# Brief: [Probes and Submarines]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n')[0]
    target_area = input_data.strip('target area: ').split(', ')

def parse_target_area(target_area):
    x1, x2 = map(int, target_area[0].strip('x=').split('..'))
    y1, y2 = map(int, target_area[1].strip('y=').split('..'))
    min_x = min(x1, x2)
    min_y = min(y1, y2)
    max_x = max(x1, x2)
    max_y = max(y1, y2)
    coordinates = {'max_x': max_x, 'min_x':min_x,
                    'max_y': max_y, 'min_y': min_y}
    return coordinates

coords = parse_target_area(target_area)
ans_p1 = (coords['min_y'] + 1) * coords['min_y'] // 2
print("Part 1:", ans_p1)

def simulate_probe(coordinates, velocity, start = (0, 0)):
    x, y = start
    v_x, v_y = velocity
    # Define boundaries of the target area
    min_x = coordinates['min_x']
    max_x = coordinates['max_x']
    min_y = coordinates['min_y']
    max_y = coordinates['max_y']

    while x <= max_x and y >= min_y:
        x, y = x + v_x, y + v_y
        v_y -= 1
        if v_x > 0:
            v_x -= 1
        elif v_x < 0:
            v_x += 1
        elif v_x == 0:
            v_x += 0

        if min_x <= x <= max_x and min_y <= y <= max_y:
            return velocity
    return None

iter = 0
valid_velocity = set()
velocity_range = 700
for vy in range(-velocity_range, velocity_range):
    for vx in range(0, velocity_range):
        velocity = simulate_probe(coords, (vx, vy), (0,0))
        iter += 1
        # print(iter)
        if velocity != None:
            valid_velocity.add(velocity)

print("Part 2:", len(valid_velocity))