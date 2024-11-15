# Advent of Code - Day 21, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/21
# Solution by: [abbasmoosajee07]
# Brief: [String Scrambler, P2]

import os, re
import itertools
import numpy as np

# Different approach taken from Part 1 of the question, more brute force
D21_file = 'Day21_input.txt'
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)


# Reading input
with open(D21_file_path) as f:
    instructions = f.read().strip().splitlines()

# Define functions to manipulate the word
def swap(x, y, word):
    word = list(word)
    word[x], word[y] = word[y], word[x]
    return ''.join(word)

def swap_letters(a, b, word):
    return word.replace(a, '?').replace(b, a).replace('?', b)

def rotate(direction, steps, word):
    steps %= len(word)
    if direction == 'right':
        return word[-steps:] + word[:-steps]
    return word[steps:] + word[:steps]

def rotate_position(letter, word):
    index = word.index(letter)
    steps = index + 2 if index >= 4 else index + 1
    return rotate('right', steps, word)

def reverse_positions(x, y, word):
    return word[:x] + word[x:y+1][::-1] + word[y+1:]

def move_position(x, y, word):
    letter = word[x]
    word = word[:x] + word[x+1:]
    return word[:y] + letter + word[y:]

# Part 1 and Part 2 logic
initial = 'abcdefgh'

for perm in itertools.permutations(initial):
    scrambled = ''.join(perm)
    original = ''.join(perm)

    for instruction in instructions:
        tokens = instruction.split()

        if tokens[0] == 'swap':
            if tokens[1] == 'position':
                scrambled = swap(int(tokens[2]), int(tokens[-1]), scrambled)
            else:
                scrambled = swap_letters(tokens[2], tokens[-1], scrambled)
        
        elif tokens[0] == 'rotate':
            if tokens[1] == 'based':
                scrambled = rotate_position(tokens[-1], scrambled)
            else:
                scrambled = rotate(tokens[1], int(tokens[2]), scrambled)
        
        elif tokens[0] == 'reverse':
            scrambled = reverse_positions(int(tokens[2]), int(tokens[-1]), scrambled)
        
        elif tokens[0] == 'move':
            scrambled = move_position(int(tokens[2]), int(tokens[-1]), scrambled)
        
        else:
            print("Unexpected instruction:", instruction)

    if original == initial:
        print("Part 1:", scrambled)
    
    if scrambled == 'fbgdceah':
        print("Part 2:", original)
        break
