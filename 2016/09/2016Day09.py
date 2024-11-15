# Advent of Code - Day 9, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/9
# Solution by: [abbasmoosajee07]
# Brief: [Compressed Data Handling]

import os

# Define the input file path
D9_file = 'Day09_input.txt'
D9_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D9_file)

# Read input file
with open(D9_file_path) as file:
    input_lines = file.read().strip()

def parse_marker(marker):
    """Parse the marker of the format (AxB) and return A and B as integers."""
    marker = marker[1:-1]
    A, B = map(int, marker.split('x'))
    return A, B

def calculate_decompressed_length(input_string):
    total_length = 0
    i = 0
    length = len(input_string)

    while i < length:
        if input_string[i] == '(':
            # Find the closing parenthesis
            end_marker = input_string.find(')', i)
            if end_marker == -1:
                print("No closing parenthesis found; exiting.")
                break  # No closing parenthesis found; exit
            
            # Parse the marker (AxB)
            marker = input_string[i:end_marker + 1]  # Include the closing parenthesis
            A, B = parse_marker(marker)
            i = end_marker + 1  # Move past the marker

            # Calculate the length of the repeated section
            total_length += B * A  # Multiply by the length of repeated section (A)
            i += A  # Move past the repeated section
        else:
            # Regular character, just increase the total length
            total_length += 1
            i += 1

    return total_length

def calculate_recursive_length(input_string):
    total_length = 0
    i = 0
    length = len(input_string)

    while i < length:
        if input_string[i] == '(':
            # Find the closing parenthesis
            end_marker = input_string.find(')', i)
            if end_marker == -1:
                print("No closing parenthesis found; exiting.")
                break  # No closing parenthesis found; exit
            
            # Parse the marker (AxB)
            marker = input_string[i:end_marker + 1]  # Include the closing parenthesis
            A, B = parse_marker(marker)
            i = end_marker + 1  # Move past the marker

            # Calculate the length of the repeated section recursively
            repeated_section = input_string[i:i + A]
            total_length += B * calculate_recursive_length(repeated_section)  # Recursive call
            i += A  # Move past the repeated section
        else:
            # Regular character, just increase the total length
            total_length += 1
            i += 1

    return total_length

# Calculate lengths
part1_length = calculate_decompressed_length(input_lines)
part2_length = calculate_recursive_length(input_lines)

# Print results
print("Part 1 - Decompressed length:", part1_length)
print("Part 2 - Recursive decompressed length:", part2_length)
