# Advent of Code - Day 8, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/8
# Solution by: [abbasmoosajee07]
# Brief: [Dealing with strings and special characters]

import os
import re
import numpy as np

D8_file = 'Day08_input.txt'
D8_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D8_file)

with open(D8_file_path) as file:
    strings_list = file.read()

strings_list = strings_list.splitlines()
# print(strings_list)


def difference_in_characters(strings):
    total_code_chars = 0
    total_memory_chars = 0
    encoded_total = 0
    
    for string in strings:
        # Count the number of characters in code (literal form)
        code_chars = len(string)

        # Use eval() to interpret the string as it would be in memory
        memory_chars = len(eval(string))  # eval interprets the string and removes escape sequences
        encoded_string = '"' + string.replace('\\', '\\\\').replace('"', '\\"') + '"'

        total_code_chars += code_chars
        total_memory_chars += memory_chars
        encoded_total += len(encoded_string) 
        
        og_diff = total_code_chars - total_memory_chars
        new_diff =  encoded_total- total_code_chars
        
    return og_diff, new_diff

og_diff, new_diff = difference_in_characters(strings_list)
print(f"Difference in characters for whole string list: {og_diff}")

print(f"The difference in encoded length is: {new_diff}")

