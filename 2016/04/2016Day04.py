# Advent of Code - Day 4, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/4
# Solution by: [abbasmoosajee07]
# Brief: [Validating Strings and using Checksums]

import os
import re
import pandas as pd
import numpy as np
from collections import Counter

D4_file = 'Day04_input.txt'
D4_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D4_file)

with open(D4_file_path) as file:
    input = file.read()
    
input = input.splitlines()


def parse_room_info(room):
    # Splitting the string by dashes and brackets
    elements = room.rsplit('-', 1)  # First split on the last dash
    word_part = elements[0].split('-')  # Split the word part by dashes
    letters = ''.join(filter(str.isalpha, word_part))

    ID, checksum = elements[1].split('[')  # Split the number and the checksum
    checksum = checksum.rstrip(']')  # Remove the closing bracket from the checksum
        
    # Return in the required format
    return [letters, ID, checksum, word_part]

room_list = input

"""--------------------------Part 1----------------------------------"""
def check_real_room(room_details):
    room_n = room_details
    
    letter_count = Counter(room_n[0])
    sorted_letters = sorted(letter_count.items(), key=lambda x: (-x[1], x[0]))
    top_five_letters = sorted_letters[:5]
    top_five_letters = [letter for letter, count in top_five_letters for _ in range(count)]

    letters_check = set(top_five_letters) == set(room_details[2])
    
    if letters_check == True:
        ID = room_details[1]
    else:
        ID = 0
    
    return ID


total = 0
for room_no in range(len(room_list)):
    room_n = room_list[room_no]
    room_info = parse_room_info(room_n)
    room_check = check_real_room(room_info)
    total += int(room_check)

print(f"Part 1: The sum of real room IDs is {total}")

"""--------------------------Part 2----------------------------------"""

def shift_letters(text, shift):
    shifted_text = ""
    
    for char in text:
        if char.isalpha():  # Check if the character is a letter
            # Calculate the shift for both uppercase and lowercase letters
            shift_base = ord('A') if char.isupper() else ord('a')
            # Shift the letter and wrap around using modulo 26
            shifted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            shifted_text += shifted_char
        else:
            shifted_text += char  # Keep non-alphabet characters unchanged
    
    return shifted_text

total = 0
room_names = pd.DataFrame()
for room_no in range(len(room_list)):
    room_n = room_list[room_no]
    room_info = parse_room_info(room_n)
    room_name = [shift_letters(text, int(room_info[1])) for text in room_info[3]]
    room_nameID = pd.DataFrame([[room_info[1], room_name]], columns = ['ID', 'Name'])
    
    room_names = pd.concat([room_names, room_nameID], ignore_index=True)

# Define the list of keywords to filter by
room_keywords = ['northpole','object']

# Filter rows where 'Name' contains any of the keywords
part2_df = room_names[room_names['Name'].apply(lambda x: any(room_keywords in x for room_keywords in room_keywords))]

# Show the filtered DataFrame
print(part2_df)