# Advent of Code - Day 9, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/9
# Solution by: [abbasmoosajee07]
# Brief: [Calculating Marbles in a circle]

import os, re
from collections import deque

# Load the input data from the specified file path
D9_file = "Day09_input.txt"
D9_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D9_file)

# Read and sort input data into a grid
with open(D9_file_path) as file:
    input_data = file.read().strip().split(';')

def marble_mania(players, marbles):
    scores = [0] * players
    circle = deque([0])

    for marble in range(1, marbles + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    
    return max(scores)

# Example Usage
# 30 players; last marble is worth 5807 points
players = int(re.search(r'\d+', input_data[0]).group())
last_marbles = int(re.search(r'\d+', input_data[1]).group())

high_score_P1 = marble_mania(players, last_marbles)
print(f"Part 1: High score: {high_score_P1}")

last_marbles_100 = last_marbles * 100
high_score_P2 = marble_mania(players, last_marbles_100)
print(f"Part 2: High score: {high_score_P2}")

