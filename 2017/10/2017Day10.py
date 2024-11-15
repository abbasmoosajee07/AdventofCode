# Advent of Code - Day 10, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/10
# Solution by: [abbasmoosajee07]
# Brief: [Hash a number list]

from functools import reduce
import os
# Load the input file
D10_file = 'Day10_input.txt'
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Load input data from the specified file path
with open(D10_file_path) as file:
    input_string = file.read().splitlines()

def build_hash(num_list, length, skip_size, current_position):
    """Single round of the Knot Hash algorithm."""
    list_len = len(num_list)
    
    # Extract sublist with circular wrapping and reverse it
    sub_list = [num_list[(current_position + i) % list_len] for i in range(length)]
    sub_list.reverse()
    
    # Replace the original elements in the circular list
    for i in range(length):
        num_list[(current_position + i) % list_len] = sub_list[i]
    
    # Update position and skip size
    current_position = (current_position + length + skip_size) % list_len
    skip_size += 1
    
    return num_list, current_position, skip_size

def knot_hash(input_string):
    """Computes the Knot Hash for a given input string."""
    # Step 1: Convert input string to ASCII codes and append the suffix
    ascii_lengths = [ord(c) for c in input_string] + [17, 31, 73, 47, 23]
    
    # Step 2: Initialize the list, position, and skip size
    num_list = list(range(256))
    current_position = 0
    skip_size = 0

    # Step 3: Perform 64 rounds
    for _ in range(64):
        for length in ascii_lengths:
            num_list, current_position, skip_size = build_hash(num_list, length, skip_size, current_position)

    # Step 4: Create the dense hash by XOR-ing blocks of 16 numbers
    dense_hash = []
    for block_start in range(0, 256, 16):
        xor_result = 0
        for i in range(16):
            xor_result ^= num_list[block_start + i]
        dense_hash.append(xor_result)

    # Step 5: Convert dense hash to hexadecimal format
    hex_hash = ''.join(f'{num:02x}' for num in dense_hash)
    # print(dense_hash)
    return hex_hash

def Part_1():
    # Initialize list and lengths
    num_list = list(range(256))
    lengths = [int(num) for num in input_string[0].split(',')]

    # Initialize position and skip variables
    skip_size = 0
    current_position = 0
    hashed_list = num_list

    # Process each length in the lengths list
    for length in lengths:
        hashed_list, current_position, _ = build_hash(hashed_list, length, skip_size, current_position)
        skip_size += 1

    P1_ans = hashed_list[0] * hashed_list[1]
    # Calculate and print the product of the first two elements
    
    print(f"Part 1: {P1_ans}")

def Part_2():
    input = input_string[0]
    ans_p2 = knot_hash(input)
    print("Part 2:", ans_p2)
    

if __name__ == "__main__":
    Part_1()
    Part_2()
