# Advent of Code - Day 1, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Summing Numbers]


import os, copy
from collections import Counter

# Load the input data from the specified file path
D1_file = "Day01_input.txt"
D1_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D1_file)

with open(D1_file_path) as file:
    input_data = file.read().strip().split('\n')

print(input_data)

def calc_frequency(strings, freq_list = []):
    frequency = 0
    for str in strings:
        num = int(str)
        frequency += num
        freq_list.append(frequency)
    return frequency, freq_list

freq_P1, _ = calc_frequency(input_data)
print(f"Part 1: Cumulative Frequency is {freq_P1}")

flag = False
frequency = 0
pos = -1
freq_list = []
iter = 0
while flag == False:
    pos = (pos + 1) % len(input_data)
    num = int(input_data[pos])
    frequency += num
    iter += 1
    # print(iter, pos, frequency)
    if frequency in freq_list:
        flag = True
    else:
        freq_list.append(frequency)

print(f"Part 1: Cumulative Frequency is {frequency}")
