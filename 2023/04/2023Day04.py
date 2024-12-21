"""Advent of Code - Day 4, Year 2023
Solution Started: Dec 20, 2024
Puzzle Link: https://adventofcode.com/2023/day/4
Solution by: abbasmoosajee07
Brief: [Card Games w/ recursion]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D04_file = "Day04_input.txt"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

# Read and sort input data into a grid
with open(D04_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list: list) -> dict:
    card_games = {}
    for game in input_list:
        game_no, cards = game.split(': ')
        game_no = int(re.findall(r'-?\d+', game_no)[0])
        winning_str, available_str = cards.split('|')
        win_no = list(map(int, re.findall(r'-?\d+', winning_str)))
        your_no = list(map(int, re.findall(r'-?\d+', available_str)))
        card_games[game_no] = {'win':win_no, 'your':your_no}
    return card_games

def basic_game(game_dict: dict) -> tuple[dict, int]:
    total_points = 0
    match_dict = {}
    for game_no, cards in game_dict.items():
        total_matches = set(cards['win']) & set(cards['your'])
        match_dict[game_no] = {'match':len(total_matches),'count':1}
        if len(total_matches) > 0:
            total_points += 2 ** (len(total_matches) - 1)
            match_dict[game_no] = {'match':len(total_matches),'count':1}
    return match_dict, total_points

def complex_game(win_cards: dict) -> int:
    def process_game(game_no: int, match: int):
        """Recursive helper function to process a game and its copies."""
        nonlocal total_cards
        win_copies = games_list[game_no: match + game_no]
        for win_game in win_copies:
            win_cards[win_game]['count'] += 1
            # Recursively process the copies
            process_game(win_game, win_cards[win_game]['match'])
        return len(win_copies)

    total_cards = 0
    games_list = list(win_cards.keys())
    for game_no, properties in win_cards.items():
        match = properties['match']
        # Process the current game recursively
        process_game(game_no, match)
        total_cards += win_cards[game_no]['count']
    return total_cards

hand_of_cards = parse_input(input_data)
win_cards, points_p1 = basic_game(hand_of_cards)
print("Part 1:", points_p1)

points_p2 = complex_game(win_cards)
print("Part 2:", points_p2)