# Advent of Code - Day 4, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/4
# Solution by: [abbasmoosajee07]
# Brief: [Identifying duplicate strings in a password list]

import os
import re
import pandas as pd
import numpy as np
from collections import Counter

D4_file = 'Day04_input.txt'
D4_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D4_file)

with open(D4_file_path) as file:
    input = file.read().splitlines()

def has_duplicates(text):
    words = text.split()  # Split the string into words
    return len(words) != len(set(words))

def has_anagrams(text):
    words = text.split()
    seen = set()
    
    for word in words:
        sorted_word = ''.join(sorted(word))  # Sort characters of each word
        if sorted_word in seen:
            return True  # An anagram is found
        seen.add(sorted_word)
    
    return False  # No anagrams found

def count_valid_passwords(password_list, function):
    valid_password = 0

    for phrase in password_list:
        
        valid = function(phrase)
                
        if valid == True:
            valid_password += 0
        else:
            valid_password += 1
        
    return valid_password

P1_count = count_valid_passwords(input, has_duplicates)
print(f"Part 1: Number of valid password strings, exluding duplicates: {P1_count}")

P2_count = count_valid_passwords(input, has_anagrams)
print(f"Part 2: Number of valid password strings, excluding anagrams: {P2_count}")
