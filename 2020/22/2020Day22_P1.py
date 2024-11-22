# Advent of Code - Day 22, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Card Games, V1]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid
with open(D22_file_path) as file:
    input_data = file.read().strip().split('\n\n')
    player_1_init = [int(row) for row in input_data[0].strip('Player 1: ').split('\n') if row != '']
    player_2_init = [int(row) for row in input_data[1].strip('Player 2: ').split('\n') if row != '']

def play_round(player_1, player_2):
    p1_card = player_1[0]
    player_1.pop(0)

    p2_card = player_2[0]
    player_2.pop(0)

    if p1_card > p2_card:
        player_1.append(p1_card)
        player_1.append(p2_card)
    elif p1_card < p2_card:
        player_2.append(p2_card)
        player_2.append(p1_card)
    return player_1, player_2

player_1_cards = player_1_init
player_2_cards = player_2_init

for round in range(10**7):
    
    player_1_cards, player_2_cards = play_round(player_1_cards, player_2_cards)
    if len(player_1_cards) <= 0:
        winning_cards = player_2_cards
        break
    elif len(player_2_cards) <= 0:
        winning_cards = player_1_cards
        break

# Calculate Winning Score
total_score = 0
len_cards = len(winning_cards)
for pos_n, card in enumerate(winning_cards):
    pos = len_cards - pos_n
    total_score += card * pos

print("Part 1:", total_score)