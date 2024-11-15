# Advent of Code - Day 19, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/19
# Solution by: [abbasmoosajee07]
# Brief: [Circular lists and stealing elves, P1]

import numpy as np
import pandas as pd

def create_elf_df(no_of_elves, gifts_per_elf):

    elves_gifts = [[i, gifts_per_elf] for i in range(1, no_of_elves + 1)]
    elves_df = pd.DataFrame(elves_gifts, columns = ['Elf', 'Gifts'])
    
    return elves_df

def get_neighbors(numbers, target_number):
    # Get the number at the index
    index = numbers.index(target_number)

    number = numbers[index]
    
    # Calculate the left and right neighbors using modular arithmetic
    right = numbers[(index - 1) % len(numbers)]
    left = numbers[(index + 1) % len(numbers)]
    
    return number, right, left

def steal_gifts(elves_df, target_elf):
    
    # Create a copy of the slice (if slicing was done earlier)
    elves_df = elves_df.copy()

    # Get the current elves and their neighbors
    current_elves = elves_df['Elf'].tolist()  # Convert to a list
    _, _, Elf_L = get_neighbors(current_elves, target_elf)
    # print(target_elf, Elf_L)
    
    # Get the gifts from the target elf and its left neighbor
    neighbor_elf_gifts = elves_df.loc[elves_df['Elf'] == Elf_L, 'Gifts'].values[0]

    # Update the target elf's gifts
        # Using .values[0] instead of .iloc[0]
    elves_df.loc[elves_df['Elf'] == target_elf, 'Gifts'] += neighbor_elf_gifts
    # print(elves_df)

    elves_df.loc[elves_df['Elf'] == Elf_L, 'Gifts'] -= neighbor_elf_gifts  # This line should work
    # print(elves_df)

    elves_df = elves_df[elves_df['Elf'] != Elf_L]
    # print(elves_df)

    return elves_df


no_elves = 5 # Your Input
elves_df = create_elf_df(no_elves, 1)

active_elf_df = elves_df
active_elf = 1

while len(active_elf_df) > 1:
    active_elf_df = steal_gifts(active_elf_df, active_elf)
    
    current_elves = active_elf_df['Elf'].tolist()  # Convert to a list
    _, _, next_elf = get_neighbors(current_elves, active_elf)
    
    active_elf = next_elf


print(f"The properties of the remaining elf\n{active_elf_df}")
