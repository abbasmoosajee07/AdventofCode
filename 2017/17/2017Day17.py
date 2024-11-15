# Advent of Code - Day 17, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/17
# Solution by: [abbasmoosajee07]
# Brief: [Spinning Number Lists]

import os, copy
from collections import deque

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

with open(D17_file_path) as file:
    input_data = file.read()
"""-----------------Part 1: Create Function------------------"""

def spinlock(lst, insert, last_index, spin):
    # Create a deep copy of the list to modify
    new_list = copy.deepcopy(lst)
    
    # Calculate the new index to insert the new value
    new_index = (last_index + spin + 1) % len(lst)

    # Insert the new value at the calculated index + 1 (which is the next position)
    new_list.insert(new_index + 1, insert)  # Modify the copied list
    return new_list, new_index  # Return the modified list and the new index

buffer = int(input_data)
num_list = [0]  # Start with the initial value 0
iterations = 2017
# Initialize the last index
last_index = 0

# Perform the iterations for the spinlock
for num in range(1, iterations + 1):  # Start from 1 to 10
    num_list, last_index = spinlock(num_list, num, last_index, buffer)  # Use the updated list and last index for each insertion


# # Find the index of 2017 and print the value that follows it
idx = num_list.index(iterations)
print(f"Part 1: Value after {iterations} is {num_list[idx + 1]}")  # This will print the value that comes after 2017
"""-----------------Part 2: Using Existing Libraries------------------"""


spinlock_2 = deque([0])

for i in range(1, 50000001):
    spinlock_2.rotate(-buffer)
    spinlock_2.append(i)

# print(spinlock_2[spinlock_2.index(0) + 1])

# Find the index of 0 and print the value that follows it
P2_idx = spinlock_2[(spinlock_2.index(0) + 1) % len(spinlock_2)]
print(f"Part 2: {P2_idx}")
