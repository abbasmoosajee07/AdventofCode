"""Advent of Code - Day 19, Year 2024
Solution Started: Dec 19, 2024
Puzzle Link: https://adventofcode.com/2024/day/19
Solution by: abbasmoosajee07
Brief: [Building words using blocks]
"""

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_input(input_list: list):
    patterns = []
    for word in input_list[0].split(','):
        word = word.replace(' ','')
        patterns.append(word)

    target_words = input_list[1].split('\n')
    return patterns, target_words


def count_ways_to_build(target_string, word_list, memo):
    if target_string in memo:
        return memo[target_string], memo
    
    total_ways = 0
    if not target_string:
        total_ways = 1
    
    for word in word_list:
        if target_string.startswith(word):
            ways, memo = count_ways_to_build(target_string[len(word):], word_list, memo)
            total_ways += ways
    
    memo[target_string] = total_ways
    return total_ways, memo


def find_valid_towels(word_list:list, patterns: list):
    valid_count = 0
    total_combo = 0
    build_paths = {}
    for word in word_list:
        possible_combos, build_paths = count_ways_to_build(word, patterns, build_paths)
        if possible_combos > 0:
            valid_count += 1
        total_combo += possible_combos
    return valid_count, total_combo

available, desired = parse_input(input_data)
ans_p1, ans_p2 = find_valid_towels(desired, available)
print("Part 1:", ans_p1)
print("Part 2:", ans_p2)
