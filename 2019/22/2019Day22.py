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
        self.big_deck = 119315717514047
        self.shuffle_times = 101741582076661

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

    def shuffle_deck(self, deck_size: int, target_card: int, visualize: bool = False):
        deck = list(range(deck_size))

        for command, value in self.shuffle_commands:
            if command == 'cut':
                deck = deck[value:] + deck[:value]  # Cut operation
            elif command == 'increment':
                new_deck = [None] * deck_size
                for i, card in enumerate(deck):
                    new_deck[(i * value) % deck_size] = card
                deck = new_deck  # Deal with increment
            elif command == 'new stack':
                deck.reverse()   # Deal into new stack

            if visualize:
                print(command, value if command != 'new stack' else '')
                print(deck)

        target_card_pos = next(pos for pos, num in enumerate(deck) if num == target_card)
        return deck, target_card_pos

    def modular_shuffle(self, deck_size: int, target_card: int, visualize: bool = False):
        init_card = target_card
        for command, shift in self.shuffle_commands:
            original_position = target_card

            if command == 'cut':
                target_card = (target_card - shift) % deck_size
            elif command == "increment":
                target_card = (shift * target_card) % deck_size
            elif command == "new stack":
                target_card = deck_size - target_card - 1

            if visualize:
                print(f"After {command} {shift if command != 'new stack' else ''}: \n",
                        f"Card({init_card}) Moved {original_position} -> {target_card}")

        return target_card

cards = Space_Cards(input_data)

final_pos = cards.modular_shuffle(10007, 2019)
print("Part 1:", final_pos)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
