# Advent of Code - Day 7, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/7
# Solution by: [abbasmoosajee07]
# Brief: [ABBA text selection]

import os
import re

# Define the input file path
D7_file = 'Day07_input.txt'
D7_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D7_file)

# Read input file
with open(D7_file_path) as file:
    input_lines = file.read().splitlines()

def separate_text(text):
    # Use regex to find text outside and inside brackets
    outside = re.findall(r'([^\[\]]+)', text)
    inside = re.findall(r'\[([^\[\]]+)\]', text)
    return outside, inside

def has_abba(sequence):
    # Check for ABBA patterns in a sequence
    return any(sequence[i] != sequence[i + 1] and 
               sequence[i] == sequence[i + 3] and 
               sequence[i + 1] == sequence[i + 2] 
               for i in range(len(sequence) - 3))

def supports_tls(text_string):
    outside, inside = separate_text(text_string)
    return any(has_abba(s) for s in outside) and not any(has_abba(s) for s in inside)

# Part 1
tls_count = sum(supports_tls(line) for line in input_lines)
print(f"Part 1: The number of IPs available: {tls_count}")

def has_aba(sequence):
    # Find ABA patterns in the sequence
    return {sequence[i:i+3] for i in range(len(sequence) - 2) 
            if sequence[i] == sequence[i + 2] and sequence[i] != sequence[i + 1]}

def supports_ssl(text_string):
    outside, inside = separate_text(text_string)
    aba_patterns = set().union(*(has_aba(s) for s in outside))
    return any(aba[1] + aba[0] + aba[1] in s for s in inside for aba in aba_patterns)

# Part 2
ssl_count = sum(supports_ssl(line) for line in input_lines)
print(f"Part 2: The number of IPs that support SSL: {ssl_count-tls_count}")
