# Advent of Code - Day 1, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Moving on a grid like the logo turtle]

import os
import re
import pandas as pd
import numpy as np

D1_file = 'Day01_input.txt'
D1_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D1_file)

with open(D1_file_path) as file:
    directions = file.read()
    
directions = directions.split(',')
# print(directions)

def parse_direction(instruction):
    # Regex to capture the action and the four numbers (coordinates)
    match = re.search(r"(R|L)(\d+)", instruction)
    
    if match:
        direction = match.group(1)
        magnitude = int(match.group(2))
  
        # Return in the required format
        return direction, magnitude
    else:
        return ['N', 0]

location_log = pd.DataFrame()
full_trace = pd.DataFrame()
coords = [0, 0]
coord_x = 0
coord_y = 0
heading = 0

for n in range(len(directions)):
    
    instruction = directions[n]
    
    direction_n, magnitude_n = parse_direction(instruction)
    
    
    # Adjust heading based on direction_n
    if direction_n == 'R':        
        heading = (heading + 90) % 360
    else:
        heading = (heading - 90) % 360

    # Update coordinates based on heading
    if heading == 0:        # Moving north
        for step in range(magnitude_n):
            coords = [coord_x, coord_y + (step + 1)]
            coords_n = pd.DataFrame([coords], columns = ['x', 'y'])
            full_trace = pd.concat([full_trace, coords_n], ignore_index=True)
        coord_y += magnitude_n
            
    elif heading == 90:     # Moving east
        for step in range(magnitude_n):
            coords = [coord_x + (step + 1), coord_y]
            coords_n = pd.DataFrame([coords], columns = ['x', 'y'])
            full_trace = pd.concat([full_trace, coords_n], ignore_index=True)
        coord_x += magnitude_n
            
    elif heading == 180:    # Moving south
        for step in range(magnitude_n):
            coords = [coord_x, coord_y - (step + 1)]
            coords_n = pd.DataFrame([coords], columns = ['x', 'y'])
            full_trace = pd.concat([full_trace, coords_n], ignore_index=True)
        coord_y -= magnitude_n
            
    elif heading == 270:    # Moving west
        for step in range(magnitude_n):
            coords = [coord_x - (step + 1), coord_y]
            coords_n = pd.DataFrame([coords], columns = ['x', 'y'])
            full_trace = pd.concat([full_trace, coords_n], ignore_index=True)
        coord_x -= magnitude_n

    location_n = pd.DataFrame([[direction_n, magnitude_n, coord_x, coord_y, heading]], 
                              columns=['dir', 'mag', 'x', 'y', 'heading'])
    location_log = pd.concat([location_log, location_n], ignore_index=True)
      
      
last_pos_dist = location_log.iloc[-1]['x'] + location_log.iloc[-1]['y']
print(f"The final position is, x = {location_log.iloc[-1]['x']}, y = {location_log.iloc[-1]['y']},", 
        f"a total of {last_pos_dist} blocks away")

# Specify the columns to check for matches
columns_to_check = ['x', 'y']

# Identify duplicates
duplicates = full_trace[full_trace.duplicated(subset=['x', 'y'], keep='first')]

# Get the first instances of each duplicate
duplicate_coords = full_trace[full_trace[['x', 'y']].apply(tuple, 1).isin(duplicates[['x', 'y']].apply(tuple, 1))].drop_duplicates(subset=['x', 'y'], keep='first')

dupl_pos_dist = duplicates.iloc[0]['x'] + duplicates.iloc[0]['y']
print(f"The first identical position is, x = {duplicates.iloc[0]['x']}, y = {duplicates.iloc[0]['y']},", 
        f"a total of {dupl_pos_dist} blocks away")