# Advent of Code - Day 11, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/11
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

import numpy as np

def calc_power_level(x_coord, y_coord, serial):
    rack_ID = x_coord + 10
    power_level_step1 = rack_ID * y_coord
    power_level_step2 = power_level_step1 + serial
    power_level_step3 = power_level_step2 * rack_ID
    hundreds_digit = abs(power_level_step3) // 100 % 10
    final_power_level = hundreds_digit - 5
    return final_power_level

puzzle_input = 42
fuel_grid_size = 300
fuel_grid = np.zeros((fuel_grid_size, fuel_grid_size))

# Fill the grid with power levels
for y in range(fuel_grid_size):
    for x in range(fuel_grid_size):
        power_level = calc_power_level(x + 1, y + 1, puzzle_input)
        fuel_grid[y][x] = power_level

# Function to find the total power for each subgrid
def find_total_power(segment):
    max_power_list = []
    for y in range(fuel_grid_size - segment + 1):  # Ensure subgrid stays within bounds
        for x in range(fuel_grid_size - segment + 1):  # Ensure subgrid stays within bounds
            segmented_grid = fuel_grid[y:y + segment, x:x + segment]  # Correct slicing
            total_power = np.sum(segmented_grid)
            max_power_list.append([x+1, y+1, segment, total_power])  # Store (y, x, power)
    
    return np.array(max_power_list)

# Find the total power for 3x3 subgrids (example size)
max_power_list = find_total_power(3)

# Find the row index of the maximum total power in the third column (total_power)
max_row_index = np.argmax(max_power_list[:, 3])

# Retrieve the entire row based on the max value's row index
max_row = max_power_list[max_row_index]
print(max_row)  # Output the result: [y, x, power]

# Initialize a list to store max values for all subgrid sizes
max_grid_power = []

# Iterate over the range of square sizes (5 to 10)
for seg_size in range(1, 300):  # From size 5x5 to 10x10
    max_grid_power_segment = find_total_power(seg_size)

    # Find the row index of the maximum value in the third column (total_power)
    max_row_index = np.argmax(max_grid_power_segment[:, 3])

    # Retrieve the entire row based on the max value's row index
    max_row = max_grid_power_segment[max_row_index]
    # print(f"Max power for size {seg_size}x{seg_size}: {max_row}")

    # Append the result to max_grid_power
    max_grid_power.append(max_row)

# Convert the list of maximum power results to a numpy array
max_grid_list = np.array(max_grid_power)

# Find the row index of the maximum total power in the third column (total_power)
max_grid_index = np.argmax(max_grid_list[:, 3])

# Retrieve the entire row based on the max value's row index
max_grid_row = max_grid_list[max_grid_index]
print(f"Overall max power square: {max_grid_row}")