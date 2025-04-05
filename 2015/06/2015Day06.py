# Advent of Code - Day 6, Year 2015
# Solved in 2025
# Puzzle Link: https://adventofcode.com/2015/day/6
# Solution by: [abbasmoosajee07]
# Brief: [Turning lights on and off]

import os
import re
import numpy as np

D6_file = 'Day06_input.txt'
D6_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D6_file)

with open(D6_file_path) as file:
    lights_inst = file.read().split('\n')
import re
import numpy as np

def parse_instruction(instruction):
    match = re.match(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)", instruction)
    if match:
        action = match.group(1)
        x1, y1, x2, y2 = map(int, match.groups()[1:])
        return action, x1, y1, x2, y2
    return None

# Initialize matrices
light_matrix_1 = np.zeros((1000, 1000), dtype=int)
light_matrix_2 = np.zeros((1000, 1000), dtype=int)

for instruction in lights_inst:
    parsed = parse_instruction(instruction)
    if not parsed:
        continue
    action, x1, y1, x2, y2 = parsed
    
    # Use slicing to target the subregion
    region = np.s_[x1:x2+1, y1:y2+1]
    
    if action == "turn on":
        light_matrix_1[region] = 1
        light_matrix_2[region] += 1
    elif action == "turn off":
        light_matrix_1[region] = 0
        light_matrix_2[region] -= 1
        light_matrix_2[region] = np.clip(light_matrix_2[region], 0, None)
    elif action == "toggle":
        light_matrix_1[region] ^= 1  # XOR to toggle between 0 and 1
        light_matrix_2[region] += 2

# Compute sums
total_sum_1 = np.sum(light_matrix_1)
total_sum_2 = np.sum(light_matrix_2)

print("Part 1:", total_sum_1)
print("Part 2:", total_sum_2)

