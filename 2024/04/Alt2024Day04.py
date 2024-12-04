"""Advent of Code - Day 4, Year 2024
Solution Started: Dec 4, 2024
Puzzle Link: https://adventofcode.com/2024/day/4
Solution by: abbasmoosajee07
Brief: [Word Search]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D04_file = "Day04_input.txt"
D04_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D04_file)

# Read and sort input data into a grid
with open(D04_file_path) as file:
    input_data = file.read().strip().split('\n')
    word_grid = [list(row) for row in input_data]

def isValid(x, y, sizeX, sizeY):
    return 0 <= x < sizeX and 0 <= y < sizeY

def searchWord(grid, word, result_grid, directions="Both"):
    n = len(grid)
    m = len(grid[0])
    word_count = 0  # Count instances of the word

    cardinal_directions = [(1, 0), (0, -1), (0, 1), (-1, 0)]  # Cardinal directions
    diagonal_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal directions
    if directions == 'both':
        directions = cardinal_directions + diagonal_directions
    elif directions == 'cardinal':
        directions = cardinal_directions
    elif directions == 'diagonals':
        directions = diagonal_directions

    for i in range(n):
        for j in range(m):
            # Check if the first character matches
            if grid[i][j] == word[0]:
                for dirX, dirY in directions:
                    if findWordInDirection(grid, n, m, word, i, j, dirX, dirY):
                        markWordInGrid(result_grid, word, i, j, dirX, dirY)
                        word_count += 1  # Increment word count

    return result_grid, word_count

def findWordInDirection(grid, n, m, word, i, j, dirX, dirY):
    # Check if all characters of the word are within bounds and match
    for k in range(len(word)):
        newRow = i + dirX * k
        newCol = j + dirY * k

        # If the new position is out of bounds, return False
        if not (0 <= newRow < n and 0 <= newCol < m):
            return False

        # If the character does not match, return False
        if grid[newRow][newCol] != word[k]:
            return False

    # If all characters match, return True
    return True

def markWordInGrid(result_grid, word, startRow, startCol, dirX, dirY):
    # Mark the found word in the result grid
    for k in range(len(word)):
        newRow = startRow + dirX * k
        newCol = startCol + dirY * k
        result_grid[newRow][newCol] = word[k]

def count_word_instances(word_words, grid, directions='both'):
    """
    Counts the total instances of words in the grid and updates the result grid.
    """
    found_grid = [['.' for _ in row] for row in grid]
    total_count = 0

    for word in word_words:
        if word:
            found_grid, word_count = searchWord(grid, word, found_grid, directions)
            total_count += word_count

    return total_count, found_grid

target_words_p1 = ['XMAS']
grid_p1 = copy.deepcopy(word_grid)
word_count_p1, found_grid_p1 = count_word_instances(target_words_p1, grid_p1)
print(f"Part 1: {word_count_p1}")

def count_diagonal_word_matches(grid, target_words):
    """
    Count occurrences of diagonal words (and their reversed versions) in the grid.
    
    Args:
    - grid (list of list of str): The grid to search within.
    - target_words (list of str): List of target words to match (including reversed).
    
    Returns:
    - int: The count of occurrences where the diagonal words match the target (or its reverse).
    """
    Y = len(grid)
    X = len(grid[0])
    count = 0
    target_word_list = [target_words[0], target_words[0][::-1]]
    # Iterate over the grid, excluding the borders (starting from 1 and ending at Y-1 and X-1)
    for y in range(1, Y-1):
        for x in range(1, X-1):
            # Extract diagonals
            d1 = grid[y-1][x-1] + grid[y][x] + grid[y+1][x+1]  # Top-left to bottom-right
            d2 = grid[y+1][x-1] + grid[y][x] + grid[y-1][x+1]  # Top-right to bottom-left

            # Check if either diagonal matches the target word or its reverse
            if (d1 in target_word_list) and (d2 in target_word_list):
                count += 1

    return count

target_words_p2 = ['MAS']
grid_p2 = copy.deepcopy(word_grid)
word_count_p2, found_grid_p2 = count_word_instances(target_words_p2, grid_p2, directions='diagonals')
count_p2 = count_diagonal_word_matches(found_grid_p2, target_words_p2)

print(f"Part 2: {count_p2}")