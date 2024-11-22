# Advent of Code - Day 23, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/23
# Solution by: [abbasmoosajee07]
# Brief: [Crab Cups Game]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read and sort input data into a grid
with open(D23_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_num = int(input_data[0])

def play_crab_cups(cup_list, moves):
    """Simulate the Crab Cups game."""
    current_cup = cup_list[0]
    min_cup, max_cup = min(cup_list), max(cup_list)

    # Create a linked list representation as a dictionary: {cup: next_cup, ...}
    next_cup_map = dict(zip(cup_list, cup_list[1:] + [cup_list[0]]))

    for _ in range(moves):
        # Pick up three cups clockwise of the current cup
        picked_up = [next_cup_map[current_cup]]
        picked_up.append(next_cup_map[picked_up[0]])
        picked_up.append(next_cup_map[picked_up[1]])

        # Find the destination cup
        destination_cup = current_cup - 1
        while destination_cup < min_cup or destination_cup in picked_up:
            destination_cup -= 1
            if destination_cup < min_cup:
                destination_cup = max_cup

        # Place the picked-up cups clockwise of the destination cup
        next_cup_map[current_cup] = next_cup_map[picked_up[-1]]
        next_cup_map[picked_up[-1]] = next_cup_map[destination_cup]
        next_cup_map[destination_cup] = picked_up[0]

        # Update the current cup
        current_cup = next_cup_map[current_cup]

    return next_cup_map

def create_cups_list(label, extend = 0):
    starting_list = list(map(int, list(str(label))))
    if extend != 0:
        cups_list = starting_list + list(range(max(starting_list)+1, extend+1))
    else:
        cups_list = starting_list
    return cups_list


# Part One: Play with initial input and 100 moves
cups_list_p1 = create_cups_list(input_num)
cups_map_p1 = play_crab_cups(cups_list_p1, 100)
labels = [cups_map_p1[1]]
while labels[-1] != 1:
    labels.append(cups_map_p1[labels[-1]])
print('Part 1:', "".join(map(str, labels[:-1])))

# Part Two: Play with extended input and 10,000,000 moves
cups_list_p2 = create_cups_list(input_num, 1_000_000)
cups_map_p2 = play_crab_cups(cups_list_p2, 10_000_000)
score = cups_map_p2[1] * cups_map_p2[cups_map_p2[1]]
print('Part 2:', score)
