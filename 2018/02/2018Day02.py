# Advent of Code - Day 2, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Letter Math and Comparison]


import os, re
from collections import Counter

# Load the input data from the specified file path
D2_file = "Day02_input.txt"
D2_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D2_file)

with open(D2_file_path) as file:
    input_data = file.read().strip().split('\n')

def calculate_checksum(strings):
    twice_count = 0
    three_count = 0

    for str in strings:
        # Remove spaces and convert to lowercase if you want to ignore case
        input_string = str.replace(" ", "").lower()

        # Count the occurrences of each letter
        letter_count = Counter(input_string)

        has_two_letters = any(count == 2 for count in letter_count.values())
        has_three_letters = any(count == 3 for count in letter_count.values())

        if has_two_letters is True:
            twice_count += 1

        if has_three_letters is True:
            three_count += 1

    checksum = twice_count * three_count
    return checksum

checksum = calculate_checksum(input_data)
print(f"Part 1: Checksum is {checksum}")

def compare_strings(str1, str2):
    # Check if lengths are the same
    if len(str1) != len(str2):
        return False, []

    # Identify positions where the characters differ
    differences = []
    common_letters = []

    for i in range(len(str1)):
        if str1[i] != str2[i]:
            differences.append(i)
        else:
            common_letters.append(str1[i])  # Collect common letters

    # Check if there are exactly two differing positions
    if len(differences) == 1:
        return True, common_letters
    else:
        return False, []

def identify_valid_ids(strings):
    for str_1 in strings:
        for str_2 in strings:
            valid, common = compare_strings(str_1, str_2)
            if valid is True:
                common = "".join(common)
                return common

identical_letter = identify_valid_ids(input_data)
print(f"Part 2: Similar letters {identical_letter}")