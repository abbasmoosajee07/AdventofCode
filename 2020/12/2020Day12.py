# Advent of Code - Day 12, Year 2020
# Solution Started: Nov 21, 2024
# Puzzle Link: https://adventofcode.com/2020/day/12
# Solution by: [abbasmoosajee07]
# Brief: [Navigating Ships]

#!/usr/bin/env python3

import os, re, copy, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read and sort input data into a grid
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n')
    action_list = [(row[0], int(row[1:])) for row in input_data]
    action_array = np.array(action_list)


def move_ship(action_list, start):
    # Starting position and facing direction
    x, y, dir = start

    # Define directions as (dx, dy) for North, East, South, West
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # N, E, S, W

    for action, mag in action_list:
        if action == 'N':
            y += mag
        elif action == 'S':
            y -= mag
        elif action == 'E':
            x += mag
        elif action == 'W':
            x -= mag
        elif action == 'L':
            dir = (dir - (mag // 90)) % 4  # Rotate left
        elif action == 'R':
            dir = (dir + (mag // 90)) % 4  # Rotate right
        elif action == 'F':
            dx, dy = directions[dir]  # Get current direction's vector
            x += dx * mag
            y += dy * mag
    abs_dist = abs(start[0] - x) + abs(start[1] - y)
    return (x, y, dir), abs_dist

_, ans_p1 = move_ship(action_list, (0, 0, 1))
print(f"Part 1: {ans_p1}")

def move_ship_with_waypoint(action_list, start, waypoint):
    # Starting position of the ship and waypoint
    ship_x, ship_y = start
    wx, wy = waypoint

    for action, mag in action_list:
        if action == 'N':  # Move waypoint north
            wy += mag
        elif action == 'S':  # Move waypoint south
            wy -= mag
        elif action == 'E':  # Move waypoint east
            wx += mag
        elif action == 'W':  # Move waypoint west
            wx -= mag
        elif action in ('L', 'R'):  # Rotate waypoint
            for _ in range((mag // 90) % 4):
                if action == 'R':  # Clockwise rotation
                    wx, wy = wy, -wx
                else:  # Counterclockwise rotation
                    wx, wy = -wy, wx
        elif action == 'F':  # Move ship toward waypoint
            ship_x += wx * mag
            ship_y += wy * mag

    return abs(ship_x) + abs(ship_y)
ans_p2 = move_ship_with_waypoint(action_list, (0, 0), (10, 1))
print(f"Part 2: {ans_p2}")