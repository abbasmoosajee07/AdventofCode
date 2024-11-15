# Advent of Code - Day 9, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/9
# Solution by: [abbasmoosajee07]
# Brief: [Removing Garbage Characters]

import os

# Load the input file
D9_file = 'Day09_input.txt'
D9_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D9_file)


# Load input data from the specified file path
with open(D9_file_path) as file:
    input_data = file.read().splitlines()

# Initialize variables
total_score = 0
total_uncanceled_garbage = 0

# Initialize stack and counters
current_group_score = 0
is_in_garbage = False
score_stack = []
index = 0

# Process each character in the input data
while index < len(input_data[0]):
    current_char = input_data[0][index]  # Get the current character

    if current_char == "!":  # Skip the next character
        index += 1
    elif is_in_garbage:  # Handling garbage
        if current_char == ">":
            is_in_garbage = False  # End of garbage
        else:
            total_uncanceled_garbage += 1  # Count uncanceled characters in garbage
    elif current_char == "{":  # Start of a new group
        current_group_score += 1
        score_stack.append(current_group_score)  # Push current score onto the stack
    elif current_char == "<":  # Start of garbage
        is_in_garbage = True
    elif current_char == "}":  # End of a group
        current_group_score -= 1
        total_score += score_stack.pop()  # Pop and add to total score
    
    index += 1  # Move to the next character

# Print or return the result as needed
print(f"Part 1: The total score for all groups is {total_score}")
print(f"Part 2: No of non-canceled characters are within the garbage {total_uncanceled_garbage}")
