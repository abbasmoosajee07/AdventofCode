# Advent of Code - Day 22, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Creating a Node Map]

import os, re
import numpy as np
import pandas as pd

# Example file name (adjust the path as needed)
D22_file = 'Day22_input.txt'
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Load the input
with open(D22_file_path) as file:
    input_data = file.read().splitlines()
    
def parse_nodes(nodes_list):
    # List to store parsed commands
    node_properties = []

    # Standard expressions for each node pair command
    node_pattern = r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"

    for node_pair in nodes_list:
        node_match = re.match(node_pattern, node_pair)
        if node_match:
            # print(node_match)
            x, y, size, used, avail, use_p = map(int, node_match.groups())
            # print()
            node_properties.append(([x, y, size, used, avail, use_p]))
    
    return pd.DataFrame(node_properties, 
                        columns = ['x','y', "Size", "Used", "Avail", "Use%"])


def check_node_pair_availability(node_A,node_B):
    xA = node_A['x']
    yA = node_A['y']
    Size_A = node_A['Size']
    Used_A = node_A['Used']
    Avail_A = node_A['Avail']
    Use_pB = node_A['Use%']
    
    xB = node_B['x']
    yB = node_B['y']
    Size_B = node_B['Size']
    Used_B = node_B['Used']
    Avail_B = node_B['Avail']
    Use_pB = node_B['Use%']
    
    # print(node_A,node_B)
    if xA == xB and yA == yB:
        return 0
    else:
        if Used_A != 0:
            if Used_A <= Avail_B:
                return 1
            else:
                return 0
        else:
            return 0

def count_pairs(node_df):
    total_combos = len(node_df) * len(node_df)
    available_pairs = 0
    count = 0
    node_combos = []
    for n_1 in range(len(node_df)):
        node_1 = node_df.loc[n_1]
        for n_2 in range(len(node_df)):
            count += 1
            node_2 = node_df.loc[n_2]
            node_pair = check_node_pair_availability(node_1, node_2)
            
            if node_pair == 1:
                node_combos.append([n_1,n_2])
                
            available_pairs += node_pair
            
            # print( count, np.round((count/total_combos*100),3), available_pairs)
    
    return available_pairs, node_combos

    
node_df = parse_nodes(input_data)
viable_pairs, combo_df = count_pairs(node_df)
print(f"Part 1: No of Viable Pairs: {viable_pairs}")

def create_node_grid(node_df):
    x_max = max(node_df['x'])
    y_max = max(node_df['y'])
    # node_grid =  np.zeros((y_max + 1, x_max + 1))
    node_grid = [["." for _ in range(x_max + 1)] for _ in range(y_max + 1)]

    for n in range(len(node_df)):
        
        node = node_df.loc[n]
        
        node_x = node['x']
        node_y = node['y']
        Used = (node['Used'])
        Size = (node['Size'])
        Used_p = node['Use%']
        
        Avail = (node['Avail'])
        label_n = f"{Used}T/{Size}T"
        node_grid[node_y][node_x] = "."
        
        if Used >= 93:
            node_grid[node_y][node_x] = "#"      
              
        if Used == 0:
            node_grid[node_y][node_x] = 'E'
        
        if node_x == x_max and node_y == 0:
            node_grid[node_y][node_x] = "G"
            
        if node_x == 0 and node_y == 0:
            node_grid[node_y][node_x] = "T"
        
    return node_grid

node_grid = create_node_grid(node_df)
node_array = np.array(node_grid)

# for row in node_grid:
#     print(row)

