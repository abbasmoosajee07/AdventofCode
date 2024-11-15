# Advent of Code - Day 25, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/25  # Web link without padding
# Solution by: [abbasmoosajee07]
# Brief: [Count Constellations]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

# Read and sort input data into a grid
with open(D25_file_path) as file:
    input_data = file.read().strip().split('\n')

def create_num_array(input):
    num_list = []
    for num_str in input:
        nums = [int(num) for num in num_str.split(',')]
        num_list.append(nums)
    return np.array(num_list)

def find_connected_stars(star_positions, start_index, visited):
    # BFS or DFS to find all connected stars within distance 3 from `start_index`
    constellation = []
    queue = [start_index]
    visited.add(start_index)
    
    while queue:
        star_idx = queue.pop()
        constellation.append(star_idx)
        current_star = star_positions[star_idx]
        
        for i, star in enumerate(star_positions):
            if i in visited:
                continue
            # Calculate Manhattan distance
            manhattan_distance = abs(star[0] - current_star[0]) + \
                                 abs(star[1] - current_star[1]) + \
                                 abs(star[2] - current_star[2]) + \
                                 abs(star[3] - current_star[3])
            # If within range, mark as visited and add to the queue
            if manhattan_distance <= 3:
                visited.add(i)
                queue.append(i)
    
    return constellation

def count_constellations(star_positions):
    visited = set()
    constellation_count = 0
    
    for i in range(len(star_positions)):
        if i not in visited:
            # Start a new constellation from this unvisited star
            find_connected_stars(star_positions, i, visited)
            constellation_count += 1  # Increment constellation count for each unique connected group
            
    return constellation_count

# Assuming `num_array` is your input array of star positions
num_array = create_num_array(input_data)
ans_p1 = count_constellations(num_array)

print(f"Part 1: {ans_p1}")
