# Advent of Code - Day 6, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/6
# Solution by: [abbasmoosajee07]
# Brief: [Turning lights on and off]

import os
import re
import numpy as np

D6_file = 'Day06_input.txt'
D6_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D6_file)

with open(D6_file_path) as file:
    lights_inst = file.read()

lights_inst = lights_inst.splitlines()

def parse_instruction(instruction):
    # Regex to capture the action and the four numbers (coordinates)
    match = re.match(r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)", instruction)
    
    if match:
        action = match.group(1)
        x1 = int(match.group(2))
        y1 = int(match.group(3))
        x2 = int(match.group(4))
        y2 = int(match.group(5))
        
        # Return in the required format
        return [action, x1, y1, x2, y2]
    else:
        return None

instruction_matrix = []

for n in range(len(lights_inst)):
    instruction_n = lights_inst[n]
    instruction_table = parse_instruction(instruction_n)
    instruction_matrix.append(instruction_table)
instruction_matrix = np.array(instruction_matrix)

light_matrix_1 = np.zeros((1000, 1000)) 

for n in range(len(lights_inst)):
    instruction_n = instruction_matrix[n]
    
    type = instruction_n[0]    

    x1 = int(instruction_n[1])
    y1 = int(instruction_n[2])
    x2 = int(instruction_n[3])
    y2 = int(instruction_n[4])
    
    dx = (x2 - x1) + 1
    dy = (y2 - y1) + 1
    
    for xi in range(dx):
        for yi in range(dy):
            xn = x1 + xi
            yn = y1 + yi
            
            if type == "turn on":
                light_matrix_1[xn][yn] = 1
            elif type == "turn off":
                light_matrix_1[xn][yn] = 0
            else:
                light_matrix_1[xn][yn] = 1 - light_matrix_1[xn][yn] # Need to absolute it
            
        
total_sum_1 = sum(element for row in light_matrix_1 for element in row)

print("Total houses with lights on:", total_sum_1)  # Output: 45

# Create a binary matrix to represent all houes with lights 
# All lights start turned off(0)
light_matrix_2 = np.zeros((1000, 1000)) 

for n in range(len(lights_inst)):
    instruction_n = instruction_matrix[n]
    
    type = instruction_n[0]    

    x1 = int(instruction_n[1])
    y1 = int(instruction_n[2])
    x2 = int(instruction_n[3])
    y2 = int(instruction_n[4])
    
    dx = (x2 - x1) + 1
    dy = (y2 - y1) + 1
    
    for xi in range(dx):
        for yi in range(dy):
            xn = x1 + xi
            yn = y1 + yi
            
            if type == "turn on":
                light_matrix_2[xn][yn] = light_matrix_2[xn][yn] + 1
            elif type == "turn off":
                light_matrix_2[xn][yn] = light_matrix_2[xn][yn] - 1
                if light_matrix_2[xn][yn] < 0:
                    light_matrix_2[xn][yn] = 0
            else:
                light_matrix_2[xn][yn] = 2 + light_matrix_2[xn][yn] # Need to absolute it
            
        
total_sum_2 = sum(element for row in light_matrix_2 for element in row)

print("Total houses with lights on:", total_sum_2)  # Output: 45
    
