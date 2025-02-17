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

    def parse_instructions(self, init_commands: list[str]) -> list[tuple[str, int]]:
        """
        Parse the list of shuffling instructions, into a list of tuples `(commamd, shift)`
        """
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

    def shuffle_deck(self, deck_size: int, target_card: int, visualize: bool = False) -> tuple[int, list[int]]:
        """
        Shuffle the whole deck of cards
        """
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
        return target_card_pos, deck

    def modular_shuffle(self, deck_size: int, target_card: int, visualize: bool = False) -> int:
        """
        Applies a series of shuffle operations on a target card in a deck.
        """
        @staticmethod
        def __transformation_func(a: int, b: int, x: int, m: int, iterations: int = 1) -> int:
            """
            Computes the linear congruential function:
                f(x) = (a * x + b) % m
            """
            k = iterations # Number of times shuffle is applied

            if a == 1:
                # Special case: If a == 1, the denominator (1 - a) becomes zero.
                return (x + k * b) % m

            # Compute f_k(x) using modular arithmetic
            a_k = pow(a, k, m)  # Compute (a^k) % m efficiently
            sum_b = (b * (1 - a_k) * pow(1 - a, -1, m)) % m  # Modular inverse of (1 - a)

            return (a_k * x + sum_b) % m

        operation_map = {
            "cut":       lambda card, shift: __transformation_func(a=1, b=-shift, x=card, m=deck_size),
            "increment": lambda card, shift: __transformation_func(a=shift, b=0, x=card, m=deck_size),
            "new stack": lambda card, _: __transformation_func(a=-1, b=-1, x=card, m=deck_size)
        }

        initial_position = target_card  # Used for visualization only

        for command, shift in self.shuffle_commands:
            if visualize:
                original_position = target_card

            target_card = operation_map[command](target_card, shift)

            if visualize:
                print(f"After {command} {shift if command != 'new stack' else ''}:\n"
                    f"\tCard({initial_position}) moved {original_position} -> {target_card}")

        return target_card

    def giant_shuffle(self, target_pos: int, deck_size: int, iterations: int, visualize: bool = False) -> int:
        """
        Keep track of what card is at a specific target pos as the deck is shuffled, over multiple iterations
        """
        a, b = 1, 0

        operation_map = {
            "cut":       lambda x, m, a, b: (a, (b - x) % m),
            "increment": lambda x, m, a, b: (a * x, b * x % m),
            "new stack": lambda _, m, a, b: (-a % m, (m - 1 - b) % m),
        }

        for command, shift in self.shuffle_commands:

            a, b = operation_map[command](shift, deck_size, a, b)

            r = (b * pow(1 - a, deck_size - 2, deck_size)) % deck_size
            new_card = ((target_pos - r) * pow(a, iterations * (deck_size - 2), deck_size) + r) % deck_size

            if visualize:
                print(f"After {command} {shift if command != 'new stack' else ''}:")
                print(f"\tAt Position {target_pos}: {new_card}")

        return new_card

cards = Space_Cards(input_data)

final_pos = cards.modular_shuffle(10007, 2019)
print("Part 1:", final_pos)

space_shuffle = cards.giant_shuffle(2020, 119315717514047, 101741582076661)
print("Part 2:", space_shuffle)

# print(f"Execution Time = {time.time() - start_time:.5f}s")

