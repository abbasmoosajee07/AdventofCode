"""Advent of Code - Day 22, Year 2019
Solution Started: Feb 15, 2025
Puzzle Link: https://adventofcode.com/2019/day/22
Solution by: abbasmoosajee07
Brief: [Shuffling Cards]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()
# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid
with open(D22_file_path) as file:
    input_data = file.read().strip().split('\n')

class Space_Cards:
    def __init__(self, instructions: list[str]):
        self.shuffle_commands = self.parse_instructions(instructions)

    def parse_instructions(self, init_commands: list[str]):
        instructions = []
        pattern = r"(cut) (-?\d+)|(deal into new stack)|(increment) (\d+)"

        for command in init_commands:
            match = re.search(pattern, command)
            if match:
                if match.group(1):    # "cut"
                    instructions.append(("cut", int(match.group(2))))
                elif match.group(3):  # "new stack"
                    instructions.append(("new stack", None))
                elif match.group(4):  # "increment"
                    instructions.append(("increment", int(match.group(5))))
        return instructions

    def __deal_new_stack(self, visualize: bool):
        og_stack = self.deck_cards
        og_deck = list(og_stack.values())
        new_deck = og_deck[::-1]
        new_stack = {pos: num for pos, num in enumerate(new_deck)}
        self.deck_cards = new_stack
        if visualize:
            print("deal into new stack")
            print(og_deck, "Original Stack")
            print(new_deck, "New Stack")

    def __deal_increment(self, increment: int, visualize: bool):
        og_deck = self.deck_cards
        deck_size = len(og_deck)
        cards_queue = list(og_deck.values())
        new_deck = {}
        card_pos = -increment
        while cards_queue:
            card = cards_queue.pop(0)
            card_pos = (card_pos + increment) % deck_size
            new_deck[card_pos] = card
        new_deck = dict(sorted(new_deck.items()))
        self.deck_cards = new_deck
        if visualize:
            print("deal with increment", increment)
            print(list(new_deck.values()))

    def __cut_stack(self, cut_point: int, visualize: bool):
        og_stack = self.deck_cards
        og_deck = list(og_stack.values())

        cut_cards = og_deck[:cut_point]
        og_deck = og_deck[cut_point:]
        new_deck = og_deck + cut_cards
        self.deck_cards = {pos: num for pos, num in enumerate(new_deck)}
        if visualize:
            print("cut", cut_point)
            print(og_deck, "Original Deck")
            print(cut_cards, "Cut Deck")
            print(new_deck, "New Deck")

    def shuffle_deck(self, deck_size: int, visualize: bool = False):
        self.deck_cards = {num: num for num in range(deck_size)}
        for command, shift in self.shuffle_commands:
            if command == 'cut':
                self.__cut_stack(shift, visualize)
            elif command == "increment":
                self.__deal_increment(shift, visualize)
            elif command == "new stack":
                self.__deal_new_stack(visualize)
        if visualize:
            print(list(self.deck_cards.values()), "Final Stack")
        return self.deck_cards

cards = Space_Cards(input_data)
shuffled_cards = cards.shuffle_deck(10007)
print("Part 1:", next(pos for pos, num in shuffled_cards.items() if num == 2019))

# print(f"Execution Time = {time.time() - start_time:.5f}s")
