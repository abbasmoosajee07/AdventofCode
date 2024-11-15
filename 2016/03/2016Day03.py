# Advent of Code - Day 3, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Numbers check and triangle combinations]

import os
import re
import pandas as pd
import numpy as np

D3_file = 'Day03_input.txt'
D3_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D3_file)

with open(D3_file_path) as file:
    input = file.read()
    
input = input.splitlines()

"""------------------------------Part 1-----------------------------------"""

def check_triangles_1(combo_n):
    
    no_1 = combo_n[0] 
    no_2 = combo_n[1]
    no_3 = combo_n[2]
    
    combo_12 = no_1 + no_2
    combo_13 = no_1 + no_3
    combo_23 = no_2 + no_3
    # print([combo_12, combo_13, combo_23])
    
    if combo_12 > no_3:
        if combo_13 > no_2:
            if combo_23 > no_1:
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0

counter_1 = 0
num_list = []
for n in range(len(input)):
    num_n = input[n]
    num_n = [int(num) for num in num_n.split()]

    triangles = check_triangles_1(num_n)
    counter_1 += triangles
    
    num_list.append(num_n)
num_list = np.array(num_list)
    
print(f"Part 1: No. of Possible Listed Triangles: {counter_1}")
"""------------------------------Part 2-----------------------------------"""

def check_triangles_2(num_list):
    for n1 in range(len(num_list)):
        no_1 = num_list[n1] 
        
        no_2 = num_list[n1 + 1]
        no_3 = num_list[n1 + 2]
        
        combo_12 = no_1 + no_2
        combo_13 = no_1 + no_3
        combo_23 = no_2 + no_3
        # print([combo_12, combo_13, combo_23])
        
        if combo_12 > no_3:
            if combo_13 > no_2:
                if combo_23 > no_1:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0

counter_2 = 0



def is_valid_triangle(sides):
    """
    Check if a given set of 3 sides can form a valid triangle.
    """
    a, b, c = sorted(sides)
    return a + b > c

def check_triangles_2(data):

    # Initialize a counter for valid triangles
    valid_count = 0
    
    # Process the array in chunks of 3 rows
    for i in range(0, len(data), 3):
        # Extract the next 3 rows (to form column triangles)
        group = data[i:i+3]
        
        # Check triangles formed by columns in this 3-row group
        for col in range(3):
            sides = group[:, col]
            if is_valid_triangle(sides):
                valid_count += 1
    
    return valid_count


triangles = check_triangles_2(num_list)
print(f"Part 2: No. of Possible Listed Triangles: {triangles}")
