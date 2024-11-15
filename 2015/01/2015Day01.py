# Advent of Code - Day 1, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Simple (Bracket) Maths]

import os

D1_file = 'Day01_input.txt'
D1_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D1_file)

with open(D1_file_path) as file:
    apt = file.read()

floor_list = list(apt)
total_floors = len(apt)

# Initialize a counter at ground floor = 0
floor_i = 0
basement_indices = []

# Iterate through the whole apartment counting the floors as it goes along
for i in range(total_floors):

    if floor_i == -1:
        basement_indices.append(i)

    # Check if the bracket is (
    if floor_list[i] == '(': 
        floor_i += 1
    else:
        floor_i += -1
    

print(f"Instructions direct Santa to Floor {floor_i}.")

print(f"Santa first enters basement at position {basement_indices[0]}.")

