# Advent of Code - Day 22, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Card Games, V2 Recursicve Combat]

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

def game(player_1, player_2):  # player X & Y
    occur = []  # To detect infinite loops (previous round states)
    while player_1 and player_2:
        if player_1 in occur:  # Cycle detection: if the state repeats, player 1 wins
            return player_1, True  # Player 1 wins
        else:
            occur.append(player_1[:])  # Record the current state of player X's deck
        
        card_1, card_2 = player_1.pop(0), player_2.pop(0)  # Draw the top cards

        # If both players have enough cards to play a sub-game
        if card_1 <= len(player_1) and card_2 <= len(player_2):
            _, flag = game(player_1[:card_1], player_2[:card_2])  # Recursively play a sub-game
            if flag:  # If player 1 wins the sub-game
                player_1.append(card_1)
                player_1.append(card_2)
            else:  # If player 2 wins the sub-game
                player_2.append(card_2)
                player_2.append(card_1)
        else:
            # Regular round: the higher card wins
            if card_1 > card_2:
                player_1.append(card_1)
                player_1.append(card_2)
                flag = True  # Player 1 wins the round
            else:
                player_2.append(card_2)
                player_2.append(card_1)
                flag = False  # Player 2 wins the round

    # Return the winner's deck and the result flag
    return (player_1 if player_1 else player_2), flag

# Play the game and get the winner's deck
winning_cards = game(player_1_init[:], player_2_init[:])[0]

# Calculate Winning Score
total_score = 0
len_cards = len(winning_cards)
for pos_n, card in enumerate(winning_cards):
    pos = len_cards - pos_n
    total_score += card * pos

print("Part 2:", total_score)
