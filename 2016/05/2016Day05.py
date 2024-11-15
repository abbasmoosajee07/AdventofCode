# Advent of Code - Day 5, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/5
# Solution by: [abbasmoosajee07]
# Brief: [MD5 Hashcode Passwords]

import os, hashlib
D5_file = 'Day05_input.txt'
D5_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D5_file)

with open(D5_file_path) as file:
    input = file.read()
"""--------------------------Part 1----------------------------------"""
def find_password(door_id):
    password = []
    index = 0
    
    while len(password) < 8:
        # Combine Door ID with index and compute MD5 hash
        hash_input = door_id + str(index)
        hash_result = hashlib.md5(hash_input.encode()).hexdigest()
        
        # Check if the hash starts with five zeroes
        if hash_result.startswith('00000'):
            # Append the sixth character to the password
            password.append(hash_result[5])
            # print(f"Found character {hash_result[5]} at index {index}")
        
        # Increment the index
        index += 1
    
    return ''.join(password)

# Example usage:
door_id = input  # Replace "abc" with the actual Door ID
password = find_password(door_id)
print(f"Part 1: The password is: {password}")

"""--------------------------Part 2----------------------------------"""

def find_password_with_position(door_id):
    password = ['_'] * 8  # Initialize an 8-character password with placeholders
    found_positions = set()  # Track the positions that have been filled
    index = 0
    
    while len(found_positions) < 8:
        # Combine Door ID with index and compute MD5 hash
        hash_input = door_id + str(index)
        hash_result = hashlib.md5(hash_input.encode()).hexdigest()
        
        # Check if the hash starts with five zeroes
        if hash_result.startswith('00000'):
            position = hash_result[5]  # Sixth character is the position
            if position.isdigit():
                position = int(position)
                # Ensure the position is between 0 and 7 and has not been filled yet
                if position < 8 and position not in found_positions:
                    password[position] = hash_result[6]  # Seventh character is the password char
                    found_positions.add(position)  # Mark the position as filled
                    # print(f"Found character {hash_result[6]} for position {position} at index {index}")
                    # print(f"Current password: {''.join(password)}")
        
        # Increment the index for the next hash
        index += 1
    
    return ''.join(password)

# Example usage:
password = find_password_with_position(door_id)
print(f"Part 2: The password is: {password}")

