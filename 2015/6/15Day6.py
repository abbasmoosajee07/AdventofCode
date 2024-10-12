import re
import numpy as np
import os

# Define the directory and file name
directory = r'C:\Users\User\Documents\AdventofCode\2015\6'

D6_file = 'Day6_lights.txt'
D6_file_path = os.path.join(directory, D6_file)

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


# Create a binary matrix to represent all houes with lights 
# All lights start turned off(0)
light_matrix = np.zeros((1000, 1000)) 

for n in range(len(lights_inst)):
    instruction_n = instruction_matrix[n]
    
    type = instruction_n[0]    
    if type == "turn on":
        action = 1
    elif type == "turn off":
        action = 0
    else:
        action = -1  # Need to absolute it
    
    x1 = int(instruction_n[1])
    y1 = int(instruction_n[2])
    x2 = int(instruction_n[3])
    y2 = int(instruction_n[4])
    print(f"x={x2-x1},y={y2-y1}")
    
    
print(D6_file_path)
    

# toggle   = -1 and then absolute
# turn on  == 1
# turn off == 0