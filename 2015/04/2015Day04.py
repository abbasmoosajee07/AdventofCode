# Advent of Code - Day 4, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/4
# Solution by: [abbasmoosajee07]
# Brief: [Creating a mD5 Hashcode]

import hashlib, os

D4_file = 'Day04_input.txt'
D4_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D4_file)

with open(D4_file_path) as file:
    input = file.read()

def find_advent_coin(secret_key,zero_start):
    number = 1  # Start from the first positive integer

    while True:
        # Combine the secret key with the current number
        input_str = f"{secret_key}{number}".encode()  # Encode to bytes
        # Calculate the MD5 hash
        md5_hash = hashlib.md5(input_str).hexdigest()
        
        # Check if the hash starts with five zeroes
        if md5_hash.startswith(zero_start):
            return number, md5_hash  # Return the number and corresponding hash
        
        number += 1  # Increment the number

# Your puzzle input
secret_key = input

result_number_5, result_hash_5 = find_advent_coin(secret_key,"00000")

print(f"The lowest positive number that produces an MD5 hash starting with five zeroes is: {result_number_5}")
print(f"The corresponding MD5 hash is: {result_hash_5}")

result_number_6, result_hash_6 = find_advent_coin(secret_key,"000000")
print(f"The lowest positive number that produces an MD5 hash starting with six zeroes is: {result_number_6}")
print(f"The corresponding MD5 hash is: {result_hash_6}")
