"""Advent of Code - Day 2, Year 2023
Solution Started: Dec 17, 2024
Puzzle Link: https://adventofcode.com/2023/day/2
Solution by: abbasmoosajee07
Brief: [Drawing random cubes]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_games):
    game_dict = {}
    for line in input_games:
        game, all_rounds  = line.split(': ')
        game_no = int(game.strip('Game '))
        round_list = all_rounds.split('; ')
        cube_list = []
        for round in round_list:
            round_dict = {}
            for cube in round.split(', '):
                round_dict[cube.split(' ')[1]] = int(cube.split(' ')[0])
            cube_list.append(round_dict)
        game_dict[game_no] = cube_list
    return game_dict

def check_valid_games(game_dict):
    all_valid_games, cubes_power = 0, 0

    for game_no, cube_list in game_dict.items():  # Iterate through games
        has_red, has_green, has_blue = True, True, True
        min_red, min_green, min_blue = 0, 0, 0
        for cube in cube_list:  # Iterate through the list of dictionaries
            for color, count in cube.items():  # Check each cube's color and count
                color = color.lower()  # Ensure case-insensitivity

                if color == 'red':
                    min_red = max(min_red, count)
                elif color == 'green':
                    min_green = max(min_green, count)
                elif color == 'blue':
                    min_blue = max(min_blue, count)

                if has_red and has_green and has_blue:
                    if color == 'red' and count > 12:
                        has_red = False
                    elif color == 'green' and count > 13:
                        has_green = False
                    elif color == 'blue' and count > 14:
                        has_blue = False

        cubes_power += min_red * min_green * min_blue
        # If all conditions are met, the game is valid
        if has_red and has_green and has_blue:
            all_valid_games += game_no  # Add the game number to the total

    return all_valid_games, cubes_power

game_dict = parse_input(input_data)
valid_games, cubes_power = check_valid_games(game_dict)
print("Part 1:", valid_games)
print("Part 2:", cubes_power)


