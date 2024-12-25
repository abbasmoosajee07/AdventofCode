"""Advent of Code - Day 6, Year 2023
Solution Started: Dec 24, 2024
Puzzle Link: https://adventofcode.com/2023/day/6
Solution by: abbasmoosajee07
Brief: [Winning a boat race]
"""

#!/usr/bin/env python3

import os, re, copy,time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(race_info: list) -> dict:
    race_dict = {}
    time_list = list(re.findall(r'\d+',race_info[0]))
    distance_list = list(re.findall(r'\d+',race_info[1]))
    for pos, time in enumerate(time_list):
        race_dict[int(time)] = int(distance_list[pos])
    full_time = ''.join(time_list)
    full_distance = ''.join(distance_list)
    full_race = (int(full_time), int(full_distance))
    return race_dict, full_race

def win_race(time: int, distance: int) -> int:
    total_wins = 0
    for press_button in range(time):
        speed = press_button * 1
        final_distance = (time - press_button) * speed
        if final_distance > distance:
            total_wins += 1
        # print(f"{press_button=} {speed=} {final_distance} {total_wins=}")
    return total_wins

test_input = ['Time:      7  15   30', 'Distance:  9  40  200']
races, long_race = parse_input(input_data)
all_wins = []
for race_time, distance in races.items():
    race_win = win_race(race_time, distance)
    if race_win != 0:
        all_wins.append(race_win)
print("Part 1:", np.prod(all_wins))

big_race_wins = win_race(long_race[0], long_race[1])
print("Part 2:", big_race_wins)
# print(time.time() - start_time)