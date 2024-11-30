"""Advent of Code - Day 9, Year 2022
Solution Started: Nov 30, 2024
Puzzle Link: https://adventofcode.com/2022/day/9
Solution by: abbasmoosajee07
Brief: [Building Ropes]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D09_file = "Day09_input.txt"
D09_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D09_file)

# Read and sort input data into a grid
with open(D09_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_instructions(instructions):
    instruction_list = []
    for command in instructions:
        command = command.split(' ')
        direction = command[0]
        magnitude = command[1]
        instruction_list.append([direction, int(magnitude)])
    return instruction_list

def build_tail(command_list, start=(0, 0), rope_len = 1):
    """
    Simulates the movement of a rope's head and tail in a 2D grid.

    Args:
        command_list (list of tuples): List of commands in (action, magnitude) format.
        start (tuple): Starting position of the head as (x, y).

    Returns:
        int: Total number of unique positions visited by the tail.
    """
    # Initialize positions for head and tail
    head_x, head_y = start
    tail_x, tail_y = start

    # Set to track all unique positions visited by the tail
    tail_visited = set()
    tail_visited.add((tail_x, tail_y))

    # Movement dictionary: Maps actions to changes in (x, y)
    movement = {
        'U': (0, 1),   # Move up
        'D': (0, -1),  # Move down
        'L': (-1, 0),  # Move left
        'R': (1, 0)    # Move right
    }

    # Process each command in the command list
    for action, magnitude in command_list:
        dx, dy = movement[action]  # Get movement deltas
        for _ in range(magnitude):
            # Move the head
            head_x += dx
            head_y += dy

            # Move the tail to stay adjacent to the head
            if abs(head_x - tail_x) > rope_len or abs(head_y - tail_y) > rope_len:
                # Move tail closer to head in x-direction
                if head_x != tail_x:
                    tail_x += 1 if head_x > tail_x else -1
                # Move tail closer to head in y-direction
                if head_y != tail_y:
                    tail_y += 1 if head_y > tail_y else -1

            # Record the tail's position
            tail_visited.add((tail_x, tail_y))

    # Return the total number of unique positions visited by the tail
    return tail_visited, len(tail_visited)

commands = parse_instructions(input_data)
path, ans_p1= build_tail(commands)
print("Part 1:", ans_p1)

def build_rope(command_list, rope_length=10, start=(0, 0)):
    """
    Simulates the movement of a rope with multiple knots in a 2D grid.

    Args:
        command_list (list of tuples): List of commands in (action, magnitude) format.
        rope_length (int): Number of knots in the rope.
        start (tuple): Starting position of the head as (x, y).

    Returns:
        int: Total number of unique positions visited by the last knot.
    """
    # Initialize positions for all knots in the rope
    rope = [list(start) for _ in range(rope_length)]

    # Set to track all unique positions visited by the last knot
    tail_visited = set()
    tail_visited.add(tuple(rope[-1]))  # Add initial position of the last knot

    # Movement dictionary: Maps actions to changes in (x, y)
    movement = {
        'U': (0, 1),   # Move up
        'D': (0, -1),  # Move down
        'L': (-1, 0),  # Move left
        'R': (1, 0)    # Move right
    }

    # Process each command in the command list
    for action, magnitude in command_list:
        dx, dy = movement[action]  # Get movement deltas
        for _ in range(magnitude):
            # Move the head
            rope[0][0] += dx
            rope[0][1] += dy

            # Propagate movement to the rest of the rope
            for i in range(1, rope_length):
                head_x, head_y = rope[i - 1]
                tail_x, tail_y = rope[i]

                # Check if the current knot is too far from the knot ahead
                if abs(head_x - tail_x) > 1 or abs(head_y - tail_y) > 1:
                    # Move the current knot closer to the knot ahead
                    if head_x != tail_x:
                        tail_x += 1 if head_x > tail_x else -1
                    if head_y != tail_y:
                        tail_y += 1 if head_y > tail_y else -1

                    # Update the current knot's position
                    rope[i] = [tail_x, tail_y]

            # Record the last knot's position
            tail_visited.add(tuple(rope[-1]))

    # Return the total number of unique positions visited by the last knot
    return tail_visited, len(tail_visited)


path, ans_p2= build_rope(commands)
print("Part 2:", ans_p2)

# 2107 too low