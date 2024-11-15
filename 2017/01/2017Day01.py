# Advent of Code - Day 1, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Verifying numbers by calculating checksums]

import os, re
import pandas as pd
import numpy as np

D1_file = 'Day01_input.txt'
D1_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D1_file)

with open(D1_file_path) as file:
    input = file.read()
    input_list = []
    for i in range(len(input)):
        input_list.append(int(input[i]))
        


def next_digt_captcha(num_list):
    total = 0
        
    for (i) in range(len(num_list)):
        
        first_digit = num_list[i]
        
        # Force digit to circle
        if (i + 1) >= len(num_list):
            next_digit = num_list[0]
        else:
            next_digit = num_list[i + 1]
                         
        if first_digit == next_digit:
            total += first_digit
            
    return total

P1_sum = next_digt_captcha(input_list)

print(f"Part 1: The captcha sum of input is: {P1_sum}")

# Initial Guess 1 = 993; Too low
# Correct Ans = 995, need to compare last digit to first

def half_digt_captcha(num_list):
    total = 0
    length = len(num_list)
        
    for (i) in range(len(num_list)):
        
        first_digit = num_list[i]
        # Calculate the halfway index circularly using modulo
        halfway_digit = num_list[(i + length // 2) % length]

        if first_digit == halfway_digit:
            total += first_digit
            
    return total

P2_sum = half_digt_captcha(input_list)

print(f"Part 2: The captcha sum of input is: {P2_sum}")

# Part 2
# Initial Guess: 2979 too high
# Second Guess: 1561
# Correct: 1130