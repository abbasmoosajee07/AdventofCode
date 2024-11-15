# Advent of Code - Day 2, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Travelling on keypads]

import os
import re
import pandas as pd
import numpy as np

D2_file = 'Day02_input.txt'
D2_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D2_file)

with open(D2_file_path) as file:
    input = file.read()
    
input = input.split()

def action(letter):
    if letter == 'U':
        return [+0, -1]
    elif letter == 'D' :
        return [+0, +1]
    elif letter == 'L':
        return [-1, +0]
    elif letter == 'R':
        return [+1, +0]
    else:
        return [+0, +0]
    
def index_2d(data, search):
    for i, e in enumerate(data):
        try:
            return i, e.index(search)
        except ValueError:
            pass
    raise ValueError("{!r} is not in list".format(search))

def next_position(array, index):
    y = index[0]
    x = index[1]
    array_y = array[y]
    value = array_y[x]
    return value

def find_code(directions, starting_no, keypad):

    final_code = []
    for line in range(len(directions)):
        line_n = directions[line]

        for step in range(len(line_n)):

            prev_index = index_2d(keypad, starting_no)

            command = line_n[step]
            step_action = action(command)

            xn = step_action[1] + prev_index[0]
            yn = step_action[0] + prev_index[1]
            
            if xn >= len(keypad):
                xn = len(keypad)-1
            if yn >= len(keypad): 
                yn = len(keypad)-1
            if xn < 0:
                xn = 0
            if yn < 0: 
                yn = 0
            
            new_index = [xn, yn]
            new_value = next_position(keypad, new_index)
            
            if new_value == '0':
                starting_no = starting_no
                new_value = starting_no
            else:
                starting_no = new_value

        final_code.append(new_value)
    
    return final_code
    
    

keypad_1 = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]

start_point_1 = 5

final_code_1 = find_code(input, start_point_1, keypad_1)
print(f"Part 1: The code for bathroom is {final_code_1}")
        


keypad_2 = [['0', '0', '1', '0', '0'],
            ['0', '2', '3', '4', '0'],
            ['5', '6', '7', '8', '9'],
            ['0', 'A', 'B', 'C', '0'],
            ['0', '0', 'D', '0', '0']]


start_point_2 = '5'

final_code_2 = find_code(input, start_point_2, keypad_2)
print(f"Part 2: The code for bathroom is {final_code_2}")
        
