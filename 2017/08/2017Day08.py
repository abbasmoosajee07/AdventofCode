# Advent of Code - Day 8, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/8
# Solution by: [abbasmoosajee07]
# Brief: [Registry Computing, with if conditons]

import os, re
import numpy as np
import pandas as pd
import collections
import operator

# Load the input file
D8_file = 'Day08_input.txt'
D8_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D8_file)


# Load input data from the specified file path
with open(D8_file_path) as file:
    input_data = file.read().splitlines()

# print(input_data)

def parse_instructions(instruction_list):
    instruction_df = pd.DataFrame()  # Fixed typo in DataFrame variable name
    # Regular expression to parse the instruction
    pattern = r'(\w+)\s+(\w+)\s+(-?\d+)\s+if\s+(\w+)\s+([<>]=?|==|!=)\s+(-?\d+)'
    
    for instruction in instruction_list:
        # Match the instruction against the pattern
        match = re.search(pattern, instruction)

        if match:
            # Use mapping to unpack instruction match groups
            command, action, value_str, variable, operator, threshold_str = match.groups()
            
            # Convert value and threshold to integers using map
            value, threshold = map(int, (value_str, threshold_str))
            
            # # Print parsed components for debugging
            # print(f"Command: {command}, Action: {action}, Value: {value},",
            #       "Variable: {variable}, Operator: {operator}, Threshold: {threshold}")

            # Create a DataFrame for the instruction
            instruction_n = pd.DataFrame({
                "command": [command],
                "action": [action],
                "value": [value],              # Use the integer value
                "variable": [variable],
                "operator": [operator],
                "threshold": [threshold]       # Use the integer threshold
            })

            # Concatenate the instruction DataFrame to the main DataFrame
            instruction_df = pd.concat([instruction_df, instruction_n], ignore_index=True)
        else: 
            print(f"Match not found: {instruction}")
    
    return instruction_df

def check_and_create_key(dictionary, key, default_value):
    if key in dictionary:
        return dictionary  # Access the value if the key exists
    else:
        dictionary[key] = default_value  # Create the key with the default value
        return dictionary  # Return the newly created value


# Function to check conditions based on operators
def check_condition(variable, op, threshold):
    # Mapping operator symbols to functions
    operator_map = {
        ">=": operator.ge,  # Greater than or equal to
        ">": operator.gt,   # Greater than
        "<=": operator.le,  # Less than or equal to
        "<": operator.lt,   # Less than
        "==": operator.eq,  # Equal to
        "!=": operator.ne   # Not equal to
    }

    # Return the result of the operation
    if op in operator_map:
        return operator_map[op](variable, threshold)
    else:
        raise ValueError(f"Invalid operator: {op}")

# Function to ensure the dictionary has a key, initializing if not present
def check_and_create_key(dictionary, key, default_value):
    if key not in dictionary:
        dictionary[key] = default_value
    return dictionary

# Function to process each instruction and update the register dictionary
def compute_registers(instruction, dictionary, max_val):
    reg_1 = instruction["command"]
    reg_2 = instruction["variable"]

    # Ensure both keys exist in the dictionary
    dictionary = check_and_create_key(dictionary, reg_1, 0)
    dictionary = check_and_create_key(dictionary, reg_2, 0)
    
    # Check the condition based on variable, operator, and threshold
    variable = dictionary[instruction["variable"]]
    if_condition = check_condition(variable, instruction["operator"], int(instruction["threshold"]))
    
    # If condition is true, perform the action
    if if_condition:
        value_change = int(instruction["value"])
        if instruction["action"] == "inc":
            dictionary[reg_1] += value_change
        elif instruction["action"] == "dec":
            dictionary[reg_1] -= value_change
            
        new_max_key = max(dictionary, key=dictionary.get)
        new_max_val = dictionary[new_max_key]
        
        if new_max_val > max_val:
            max_val = new_max_val
            
    return dictionary, max_val

# Example function to parse input data (assuming it's defined somewhere)
input_instructions = parse_instructions(input_data)

# Dictionary to hold register values
reg_dict = {}

max_val_2 = 0
# Process each instruction in input data
for n in range(len(input_instructions)):
    
    reg_dict, max_val_2 = compute_registers(input_instructions.loc[n], reg_dict, max_val_2)

# Find the key with the maximum value in the register dictionary
max_key = max(reg_dict, key=reg_dict.get)
max_value = reg_dict[max_key]

print(f"Part 1: The maximum value is {max_value}, found in key '{max_key}'")

print(f"Part 2: The maximum value reached by any register is {max_val_2}")
