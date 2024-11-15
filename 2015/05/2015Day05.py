# Advent of Code - Day 5, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/5
# Solution by: [abbasmoosajee07]
# Brief: [Comprehending Strings]

import os
import array
import re
import numpy as np

D5_file = 'Day05_input.txt'
D5_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D5_file)

with open(D5_file_path) as file:
    naughty_list = file.read()

naughty_list = naughty_list.split()
total_kids = len(naughty_list)

deeds_type = []

def is_nice_string(deed):
    vowel_count = sum([1 for char in deed if char in "aeiou"])
    if vowel_count < 3:
        return "naughty"

    # Check for at least one double letter
    if not re.search(r'(.)\1', deed):
        return "naughty"

    # Check for forbidden substrings
    if any(substring in deed for substring in ["ab", "cd", "pq", "xy"]):
        return "naughty"

    return "nice"
    
for n in range(total_kids):
    kids_deed = naughty_list[n]
    deed_n_type = is_nice_string(kids_deed)
    deeds_type.append(deed_n_type)

print(f"Number of Nice deeds by kids: {deeds_type.count("nice")}")


def is_nice_rev(string):
    # Check for a repeated pair
    has_repeated_pair = False
    for i in range(len(string) - 1):
        pair = string[i:i+2]
        if pair in string[i+2:]:
            has_repeated_pair = True
            break

    # Check for repeating letter with one between
    has_repeat_with_one_between = False
    for i in range(len(string) - 2):
        if string[i] == string[i+2]:
            has_repeat_with_one_between = True
            break

    # Return True only if both conditions are satisfied
    return has_repeated_pair and has_repeat_with_one_between

# Example test
nice_count = sum(1 for string in naughty_list if is_nice_rev(string))

print(f"Revised Number of nice strings: {nice_count}")
