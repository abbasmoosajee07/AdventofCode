# Advent of Code - Day 16, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/16
# Solution by: [abbasmoosajee07]
# Brief: [List comprehension]

import os
import re
import pandas as pd

D16_file = 'Day16_input.txt'
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

with open(D16_file_path) as file:
    gift_list = file.read()
    
gift_list = gift_list.splitlines()

def parse_gift_info(instruction):
    # Regex pattern to extract Sue number and attributes
    regex = r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)"
    
    # Search for the pattern in the instruction
    match = re.search(regex, instruction)
    
    if match:
        # Extract Sue number
        sue_number = int(match.group(1))
        
        # Create a dictionary of attributes
        attributes_dict = {
            match.group(2): int(match.group(3)),
            match.group(4): int(match.group(5)),
            match.group(6): int(match.group(7)),
        }
                
        return attributes_dict
    
    return None  # Return None if no match is found

# Dictionary to hold combined gift information
combined_gifts = {}

# Process each aunt's gift info and combine into a single dictionary
for aunt in range(len(gift_list)):
    gift_info = parse_gift_info(gift_list[aunt])
    
    if gift_info:  # Ensure gift_info is not None
        combined_gifts[str(aunt + 1)] = gift_info

# Define expected values and conditions for each attribute
expected_conditions_1 = {
        "children": lambda x: x == 3,
        "cats": lambda x: x is None or x == 7,
        "samoyeds": lambda x: x in [2, None],
        "pomeranians": lambda x: x is None or x == 3,
        "akitas": lambda x: x in [0, None],
        "vizslas": lambda x: x in [0, None],
        "goldfish": lambda x: x is None or x == 5,
        "trees": lambda x: x is None or x == 3,
        "cars": lambda x: x in [2, None],
        "perfumes": lambda x: x in [1, None],
    }

expected_conditions_2 = {
        "children": lambda x: x == 3,
        "cats": lambda x: x is None or x > 7,
        "samoyeds": lambda x: x in [2, None],
        "pomeranians": lambda x: x is None or x < 3,
        "akitas": lambda x: x in [0, None],
        "vizslas": lambda x: x in [0, None],
        "goldfish": lambda x: x is None or x < 5,
        "trees": lambda x: x is None or x > 3,
        "cars": lambda x: x in [2, None],
        "perfumes": lambda x: x in [1, None],
    }


def find_the_aunt(aunt_dictionary, expected_conditions):
    
    # Create a new dictionary for potential aunts that match the criteria
    potential_aunts = {}

    # Iterate through the aunt dictionary
    for sue_number, attributes in aunt_dictionary.items():
        is_valid = True  # Assume the aunt is valid until proven otherwise
        
        # Check each condition against the expected values
        for key, condition in expected_conditions.items():
            if key in attributes and not condition(attributes[key]):
                is_valid = False
                break  # Exit the loop if any condition fails
        
        if is_valid:
            potential_aunts[sue_number] = attributes  # Add valid aunt to the result

    return potential_aunts

aunt_sue_1 = find_the_aunt(combined_gifts, expected_conditions_1)
aunt_sue_2 = find_the_aunt(combined_gifts, expected_conditions_2)

print(f"Part 1: The Aunt Sue who sent the present is {(aunt_sue_1)}")
print(f"Part 2: The Aunt Sue who sent the present is {(aunt_sue_2)}")