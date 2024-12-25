"""Advent of Code - Day 7, Year 2023
Solution Started: Dec 25, 2024
Puzzle Link: https://adventofcode.com/2023/day/7
Solution by: abbasmoosajee07
Brief: [Playing Cards]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_hands: list) -> dict:
    rounds_dict = {}
    for hand_no, hand in enumerate(input_hands):
        cards, bid = hand.split(' ')
        rounds_dict[cards] = int(bid)
    return rounds_dict

def find_hand_type(cards: str) -> str:
    # Count occurrences of each card
    count_list = list(Counter(cards).values())
    count_len = len(count_list)

    # Determine hand type based on counts
    if count_len == 5:
        return 'high'
    elif count_len == 4:
        return 'one' if 2 in count_list else 'unknown'
    elif count_len == 3:
        if 3 in count_list:
            return 'three'
        elif 2 in count_list:
            return 'two'
    elif count_len == 2:
        if 4 in count_list:
            return 'four'
        elif 2 in count_list:
            return 'full'
    elif count_len == 1:
        return 'five'
    
    return 'unknown'  # Default for unexpected cases

def rate_hands(rounds_data: dict) -> dict[list[str]]:
    # Define hand strength rankings
    HAND_STRENGTH = {'high': 0, 'one': 1, 'two': 2, 'three': 3, 'full': 4, 'four': 5, 'five': 6}
    seperated_rounds = {}
    # Group hands by their strength level
    grouped_hands = {}
    for hand_data, bid in rounds_data.items():
        hand_type = find_hand_type(hand_data)  # Determine the type of the hand
        hand_strength = HAND_STRENGTH[hand_type]  # Get the numerical value for hand strength
        grouped_hands.setdefault(hand_strength, []).append(hand_data)

    # Sort hands within each group by the numeric score, and sort the groups by strength
    sorted_hands = {
        strength: sorted(hands, key=lambda x: x[1])  # Sort hands by the numeric value (second element)
        for strength, hands in sorted(grouped_hands.items())  # Sort groups by hand strength
    }

    return sorted_hands

def rank_hands(rated_rounds: dict[list[str]]):
    CARD_STRENGTH = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
                        'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    all_rated_rounds = {}
    overall_rank = 0
    for no, round_list in rated_rounds.items():
        rated_hands = {}
        for cards in round_list:
            hand_list = list(cards)
            replaced_cards = [CARD_STRENGTH[card] for card in hand_list]
            rated_hands[cards] = replaced_cards
        sorted_hands = {k: v for k, v in sorted(rated_hands.items(), key=lambda item: item[1])}
        for hand in sorted_hands.keys():
            overall_rank += 1
            all_rated_rounds[hand] = overall_rank
    return all_rated_rounds


# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
#   The relative strength of each card follows this order,
#   where A is the highest and 2 is the lowest.
test_input_1 = ['32T3K 765', 'T55J5 684', 'KK677 28', 'KTJJT 220', 'QQQJA 483']
test_input_2 = ['AAAAA 765', 'AA8AA 684', '23332 28', 'TTT98 220', '23432 483', 'A23A4 20', '23456 83']
test_input_3 = ['33332 765', '2AAAA 684', '77888 28', '77788 220']

all_rounds = parse_input(input_data)
round_types = rate_hands(all_rounds)
ranked_rounds = rank_hands(round_types)
total_winnings = 0
for hand, rank in ranked_rounds.items():
    total_winnings += rank * all_rounds[hand]
print("Part 1:", total_winnings)

# Five of a kind, where all five cards have the same label: AAAAA
# Four of a kind, where four cards have the same label
#   and one card has a different label: AA8AA
# Full house, where three cards have the same label, and the
#   remaining two cards share a different label: 23332
# Three of a kind, where three cards have the same label, and the
#   remaining two cards are each different from any other card
#   in the hand: TTT98
# Two pair, where two cards share one label, two other cards share
#   a second label, and the remaining card has a third label: 23432
# One pair, where two cards share one label, and the other three cards
#   have a different label from the pair and each other: A23A4
# High card, where all cards' labels are distinct: 23456

