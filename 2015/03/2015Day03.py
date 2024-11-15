# Advent of Code - Day 3, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Moving a point]

import os 
import array
import numpy as np

D3_file = 'Day03_input.txt'
D3_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D3_file)

with open(D3_file_path) as file:
    delivery = file.read()

delivery_schedule = list(delivery)
gifts_delivered = len(delivery_schedule)

def count_houses_with_presents(directions):
    # Starting position
    x, y = 0, 0
    # Set to keep track of visited houses
    visited_houses = set()
    
    # Add starting house
    visited_houses.add((x, y))
    
    # Move based on directions
    for direction in directions:
        if direction == '^':
            y += 1  # Move north
        elif direction == 'v':
            y -= 1  # Move south
        elif direction == '>':
            x += 1  # Move east
        elif direction == '<':
            x -= 1  # Move west
        
        # Add the new position to the set of visited houses
        visited_houses.add((x, y))
    
    # Return the number of unique houses visited
    return len(visited_houses)

# Example usage
unique_houses = count_houses_with_presents(delivery)

print(f"No of Unique houses delivered by Santa: {(unique_houses)}.")


def count_houses_with_presents(directions):
    # Starting positions for Santa and Robo-Santa
    santa_x, santa_y = 0, 0
    robo_x, robo_y = 0, 0
    # Set to keep track of visited houses
    visited_houses = set()
    
    # Add starting house (both Santa and Robo-Santa deliver to the same starting house)
    visited_houses.add((santa_x, santa_y))
    
    # Loop through directions and alternate moves between Santa and Robo-Santa
    for i, direction in enumerate(directions):
        if i % 2 == 0:  # Santa's turn (even index)
            if direction == '^':
                santa_y += 1  # Move north
            elif direction == 'v':
                santa_y -= 1  # Move south
            elif direction == '>':
                santa_x += 1  # Move east
            elif direction == '<':
                santa_x -= 1  # Move west
            
            # Add Santa's new position to the set of visited houses
            visited_houses.add((santa_x, santa_y))
        else:  # Robo-Santa's turn (odd index)
            if direction == '^':
                robo_y += 1  # Move north
            elif direction == 'v':
                robo_y -= 1  # Move south
            elif direction == '>':
                robo_x += 1  # Move east
            elif direction == '<':
                robo_x -= 1  # Move west
            
            # Add Robo-Santa's new position to the set of visited houses
            visited_houses.add((robo_x, robo_y))
    
    # Return the number of unique houses visited
    return len(visited_houses)

print(f'Revised Delivery req for unique houses: {count_houses_with_presents(delivery)}')  # Output: 3

