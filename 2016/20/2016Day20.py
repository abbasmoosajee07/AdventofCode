# Advent of Code - Day 20, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/20
# Solution by: [abbasmoosajee07]
# Brief: [Identify useful IPs in list of blocked IPs]

import os, re
import numpy as np

# Example file name (adjust the path as needed)
D20_file = 'Day20_input.txt'
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Load the input
with open(D20_file_path) as file:
    input_data = file.read().split()

# Function to parse entries of the form 'X-Y' into tuples
def parse_entry(entry):
    match = re.match(r'(\d+)-(\d+)', entry)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None

# Function to process the blacklist, sort it, and add boundary limits to cover address space
def process_blacklist(blacklist):
    # Add boundary limits and sort the blacklist
    blacklist = sorted(blacklist + [(-1, -1), (2**32, 2**32)])
    return remove_overlap(blacklist)

# Function to remove overlapping or adjacent ranges in the blacklist
def remove_overlap(blacklist):
    result = []
    lo1, hi1 = blacklist[0]
    for lo2, hi2 in blacklist[1:]:
        if hi1 >= lo2 - 1:
            # Merge ranges if they overlap or touch
            hi1 = max(hi1, hi2)
        else:
            # No overlap, push the previous range and move to the next
            result.append((lo1, hi1))
            lo1, hi1 = lo2, hi2
    result.append((lo1, hi1))  # Add the last range
    return result

# Function to find the lowest allowed IP
def lowest(blacklist):
    for i in range(len(blacklist) - 1):
        _, hi1 = blacklist[i]
        lo2, _ = blacklist[i + 1]
        if hi1 + 1 < lo2:
            return hi1 + 1
    return 0

# Function to count the number of valid IPs not in the blacklist
def count_valid(blacklist):
    total_valid = 0
    for i in range(len(blacklist) - 1):
        _, hi1 = blacklist[i]
        lo2, _ = blacklist[i + 1]
        total_valid += lo2 - hi1 - 1
    return total_valid

if __name__ == "__main__":
    # Parse the input into a blacklist
    blacklist = [parse_entry(entry) for entry in input_data if parse_entry(entry) is not None]

    # Process the blacklist
    processed_blacklist = process_blacklist(blacklist)

    # Print the lowest valid IP
    print("Lowest valid IP:", lowest(processed_blacklist))

    # Print the number of valid IPs
    print("Count of valid IPs:", count_valid(processed_blacklist))
