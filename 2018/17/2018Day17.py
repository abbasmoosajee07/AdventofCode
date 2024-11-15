# Advent of Code - Day 17, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/17
# Solution by: [abbasmoosajee07]
# Brief: [Mapping Water Flow in a Garden]

import os, sys
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
sys.setrecursionlimit(10**9)  # Increase the recursion depth

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and parse the clay veins into coordinates
clay = collections.defaultdict(bool)
with open(D17_file_path) as file:
    for line in file:
        a, brange = line.strip().split(',')
        if a[0] == 'x':
            x = int(a.split('=')[1])
            y1, y2 = map(int, brange.split('=')[1].split('..'))
            for y in range(y1, y2 + 1):
                clay[(x, y)] = True
        else:
            y = int(a.split('=')[1])
            x1, x2 = map(int, brange.split('=')[1].split('..'))
            for x in range(x1, x2 + 1):
                clay[(x, y)] = True

# Determine Y boundaries for water flow
ymin, ymax = min(clay, key=lambda p: p[1])[1], max(clay, key=lambda p: p[1])[1]

# Initialize sets for flowing and settled water
settled = set()
flowing = set()

# Function to simulate water flow
def water_flow(pt, direction=(0, 1)):
    flowing.add(pt)
    below = (pt[0], pt[1] + 1)

    # Flow downward if possible
    if not clay[below] and below not in flowing and 1 <= below[1] <= ymax:
        water_flow(below)

    # Stop if it can't settle
    if not clay[below] and below not in settled:
        return False

    # Check and fill left and right directions
    left = (pt[0] - 1, pt[1])
    right = (pt[0] + 1, pt[1])

    left_filled = clay[left] or left not in flowing and water_flow(left, direction=(-1, 0))
    right_filled = clay[right] or right not in flowing and water_flow(right, direction=(1, 0))

    # Settle water if bounded on both sides
    if direction == (0, 1) and left_filled and right_filled:
        settled.add(pt)
        while left in flowing:
            settled.add(left)
            left = (left[0] - 1, left[1])
        while right in flowing:
            settled.add(right)
            right = (right[0] + 1, right[1])

    return direction == (-1, 0) and (left_filled or clay[left]) or \
           direction == (1, 0) and (right_filled or clay[right])

# Start water flow from the spring location
water_flow((500, 0))

# Calculate the results
part1_result = len([pt for pt in flowing | settled if ymin <= pt[1] <= ymax])
part2_result = len([pt for pt in settled if ymin <= pt[1] <= ymax])

print('Part 1:', part1_result)
print('Part 2:', part2_result)

# To save the complete garden grid:
def save_grid():
    # Set grid boundaries with padding
    grid_min_x = min(x for x, y in clay) - 5
    grid_max_x = max(x for x, y in clay) + 5
    grid_min_y = ymin
    grid_max_y = ymax

    # Create a grid with the dimensions of the area plus padding
    grid_width = grid_max_x - grid_min_x + 1
    grid_height = grid_max_y - grid_min_y + 1
    grid = [['.' for _ in range(grid_width)] for _ in range(grid_height)]

    # Populate the grid with clay, flowing water, and settled water
    for (x, y) in clay:
        if grid_min_x <= x <= grid_max_x and grid_min_y <= y <= grid_max_y:
            grid[y - grid_min_y][x - grid_min_x] = '#'

    for (x, y) in flowing:
        if grid_min_x <= x <= grid_max_x and grid_min_y <= y <= grid_max_y:
            grid[y - grid_min_y][x - grid_min_x] = '|'

    for (x, y) in settled:
        if grid_min_x <= x <= grid_max_x and grid_min_y <= y <= grid_max_y:
            grid[y - grid_min_y][x - grid_min_x] = '~'

    # Save the grid to a file
    grid_file_path = "garden_grid.txt"
    with open(grid_file_path, 'w') as f:
        for row in grid:
            f.write("".join(row) + '\n')

    print(f"Grid saved to {grid_file_path}")

# Call the function to save the grid
# save_grid()
