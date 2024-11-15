# Advent of Code - Day 5, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/5
# Solution by: [abbasmoosajee07]
# Brief: [String Polymers]

import os, re, copy
import numpy as np
import pandas as pd

# Load the input data from the specified file path
D5_file = "Day05_input.txt"
D5_file_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)),D5_file)  # Updated path for better compatibility

# Read and sort input data
with open(D5_file_path) as file:
    input_data = file.read().strip()
# print(input_data)

def react_polymer(string_list):
    polymer = []

    for letter in string_list:
        # Check if there is a letter in polymer to compare with
        if polymer and letter.lower() == polymer[-1].lower():
            # Remove last character if it's the opposite case of the current letter
            if (letter.isupper() and polymer[-1].islower()) or (letter.islower() and polymer[-1].isupper()):
                polymer.pop()
            else:
                polymer.append(letter)  # Same letter but not opposite case, add to polymer
        else:
            polymer.append(letter)  # No match, add to polymer

    return polymer

polymers_P1 = react_polymer(input_data)
print(f"Part 1: Length of remaining polymer units {len(polymers_P1)}")

def remove_letter(text, letter):
    return ''.join([ch for ch in text if ch.lower() != letter.lower()])

def remove_units(string_list):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    reacting_polymer = []
    
    for letter in alphabet:
        full_polymer = remove_letter(string_list, letter)
        reacted_polymer = react_polymer(full_polymer)
        reacting_polymer.append(len(reacted_polymer))

    return np.array(reacting_polymer)

reacting_P2 = remove_units(input_data)
print(f"Part 2: Shortest polymer after reacting is {min(reacting_P2)}")