# Advent of Code - Day 4, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/4
# Solution by: [abbasmoosajee07]
# Brief: [Bing Modernized]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load input data
D04_file = "Day04_input.txt"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

with open(D04_file_path, 'r') as file:
    input_data = [line.strip() for line in file.readlines()]
    numbers = [int(x) for x in input_data[0].split(',')]
    bingo_cards = input_data[2:]  # Skip the numbers line and the empty line

# Define the BingoCard class
class BingoCard:
    def __init__(self, cardRows) -> None:
        rows = [cr.replace('  ', ' ').split(' ') for cr in cardRows]
        self.grid = np.array(rows, dtype=int)

    def markCard(self, number):
        self.grid[self.grid == number] = -1

    def getScore(self, lastCalled):
        return np.sum((self.grid != -1) * self.grid) * lastCalled

    def isWinner(self):
        return any(np.sum(self.grid, axis=0) == -5) or any(np.sum(self.grid, axis=1) == -5)

# Parse bingo cards into a DataFrame with BingoCard instances
bingo_cards = [BingoCard(bingo_cards[i * 6:i * 6 + 5]) for i in range(len(bingo_cards) // 6)]
bingo_df = pd.DataFrame({
    'bingo_card': bingo_cards,  # Store BingoCard objects
    'has_won': [False] * len(bingo_cards)  # Track if a card has won
})

# Run the game
scores = []
for number in numbers:
    for idx, row in bingo_df.iterrows():
        card = row['bingo_card']
        if not row['has_won']:
            # Mark the number on the card
            card.markCard(number)

            # Check if the card wins
            if card.isWinner():
                bingo_df.at[idx, 'has_won'] = True  # Mark card as having won
                scores.append(card.getScore(number))  # Calculate and store the score

# Output results
print('Part 1:', scores[0])  # First winning card's score
print('Part 2:', scores[-1])  # Last winning card's score
