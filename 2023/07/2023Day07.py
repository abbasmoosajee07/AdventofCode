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

class Camel_Cards:
    HAND_STRENGTH = {
        'high': 0, 'one': 1, 'two': 2, 'three': 3, 'full': 4, 'four': 5, 'five': 6
    }

    CARD_STRENGTH = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    def __init__(self, joker=False):
        self.joker = joker
        if joker:
            self.CARD_STRENGTH['J'] = 1

    def find_hand_type(self, cards: str) -> str:
        """Determine the type of hand from a set of cards."""

        def evaluate_hand(card_list):
            card_count = dict(Counter(card_list))
            count_list = list(card_count.values())
            count_len = len(count_list)

            if count_len == 5:
                return 'high'
            elif count_len == 4 and 2 in count_list:
                return 'one'
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

            return 'unknown'

        if self.joker:
            possible_cards = set(self.CARD_STRENGTH.keys())
            best_hand = 'high'
            best_replacement = None

            for replacement in possible_cards:
                substituted_cards = cards.replace('J', replacement)
                current_hand = evaluate_hand(substituted_cards)
                if self.HAND_STRENGTH[current_hand] > self.HAND_STRENGTH[best_hand]:
                    best_hand = current_hand
                    best_replacement = replacement

            if best_replacement:
                cards = cards.replace('J', best_replacement)

        return evaluate_hand(cards)

    def rate_hands(self, rounds_data: dict) -> dict:
        """Group and sort hands by their strength levels."""
        grouped_hands = {}

        for hand_data, bid in rounds_data.items():
            hand_type = self.find_hand_type(hand_data)
            hand_strength = self.HAND_STRENGTH[hand_type]
            grouped_hands.setdefault(hand_strength, []).append((hand_data, bid))

        sorted_hands = {
            strength: sorted(hands, key=lambda x: x[1])  # Sort by bid values
            for strength, hands in sorted(grouped_hands.items())
        }

        return sorted_hands

    def rank_hands(self, rated_rounds: dict) -> dict:
        """Assign ranks to hands based on their strength and numeric value."""
        ranked_hands = {}
        overall_rank = 0

        for strength, hands in rated_rounds.items():
            hand_values = {
                hand[0]: [self.CARD_STRENGTH[card] for card in hand[0]]
                for hand in hands
            }

            sorted_hands = {
                k: v for k, v in sorted(hand_values.items(), key=lambda item: item[1])
            }

            for hand in sorted_hands.keys():
                overall_rank += 1
                ranked_hands[hand] = overall_rank

        return ranked_hands

    def play_game(self, card_rounds: dict) -> int:
        """Calculate the total winnings from the game."""
        rated_hands = self.rate_hands(card_rounds)
        ranked_hands = self.rank_hands(rated_hands)

        total_winnings = 0
        for hand, rank in ranked_hands.items():
            total_winnings += rank * card_rounds[hand]

        return total_winnings


card_rounds = parse_input(input_data)

# Play the game and calculate total winnings
wins_p1 = Camel_Cards().play_game(card_rounds)
print(f"Part 1: {wins_p1}")

wins_p2 = Camel_Cards(joker=True).play_game(card_rounds)
print(f"Part 2: {wins_p2}")

