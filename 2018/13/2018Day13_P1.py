# Advent of Code - Day 13, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/13
# Solution by: [abbasmoosajee07]
# Brief: [Moving Carts in a text file, P1]

import os, re, copy
import pandas as pd

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

def find_cart_positions(cart_grid):
    cart_no = 0
    cart_data = []
    cart_grid = [list(row) for row in copy.deepcopy(cart_grid)]

    for y, line in enumerate(cart_grid):
        for x, char in enumerate(line):
            if char in "^v":
                cart_no += 1
                cart_data.append({
                    "cart": cart_no,
                    "pos": char,
                    "pos_complex": complex(x, y),  # x is real, y is imaginary
                    "next_int": "left"
                })
                cart_grid[y][x] = '|'
            elif char in "<>":
                cart_no += 1
                cart_data.append({
                    "cart": cart_no,
                    "pos": char,
                    "pos_complex": complex(x, y),  # x is real, y is imaginary
                    "next_int": "left"
                })
                cart_grid[y][x] = '-'
    cart_grid = ["".join(row) for row in cart_grid]
    return cart_grid, pd.DataFrame(cart_data)

def reached_intersection(cart_position, cart_no):
    cart_data = cart_position.loc[cart_no]

    if cart_data['next_int'] == 'left':
        turn_map = {'^': '<', '>': '^', 'v': '>', '<': 'v'}
        cart_position.loc[cart_no, 'pos'] = turn_map[cart_data['pos']]
        cart_position.loc[cart_no, 'next_int'] = 'straight'

    elif cart_data['next_int'] == 'straight':
        cart_position.loc[cart_no, 'next_int'] = 'right'

    elif cart_data['next_int'] == 'right':
        turn_map = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
        cart_position.loc[cart_no, 'pos'] = turn_map[cart_data['pos']]
        cart_position.loc[cart_no, 'next_int'] = 'left'

    return cart_position

def move_cart(cart_grid, cart_position, cart_no, cart_grid_init):
    cart_position = copy.deepcopy(cart_position)
    new_grid = [list(row) for row in copy.deepcopy(cart_grid)]

    cart_data = cart_position.loc[cart_no]
    pos_complex = cart_data['pos_complex']
    direction = cart_data['pos']

    # Determine new position based on the current direction
    move_map = {'^': complex(0, -1), 'v': complex(0, 1), '<': complex(-1, 0), '>': complex(1, 0)}
    new_pos = pos_complex + move_map[direction]
    new_x, new_y = int(new_pos.real), int(new_pos.imag)

    if not (0 <= new_y < len(cart_grid) and 0 <= new_x < len(cart_grid[0])):
        print(f"Cart {cart_no} crashed by moving out of bounds to ({new_x}, {new_y}).")
        cart_position.drop(index=cart_no, inplace=True)
        return cart_grid, cart_position

    if new_grid[new_y][new_x] == '+':
        cart_position = reached_intersection(cart_position, cart_no)
    elif new_grid[new_y][new_x] == '/':
        turn_map = {'>': '^', 'v': '<', '^': '>', '<': 'v'}
        cart_position.loc[cart_no, 'pos'] = turn_map[cart_data['pos']]
    elif new_grid[new_y][new_x] == '\\':
        turn_map = {'<': '^', 'v': '>', '>': 'v', '^': '<'}
        cart_position.loc[cart_no, 'pos'] = turn_map[cart_data['pos']]

    old_x, old_y = int(pos_complex.real), int(pos_complex.imag)
    new_grid[old_y][old_x] = cart_grid_init[old_y][old_x]
    cart_position.loc[cart_no, 'pos_complex'] = new_pos
    new_grid = ["".join(row) for row in new_grid]

    return new_grid, cart_position

def check_crash(cart_position):
    crash_carts = cart_position[cart_position.duplicated(subset=['pos_complex'], keep=False)]
    if not crash_carts.empty:
        return True, crash_carts
    return False, None

cart_grid_init = open(D13_file_path).read().splitlines()
cart_path, cart_pos_init = find_cart_positions(cart_grid_init)

cart_grid, cart_pos = cart_grid_init, cart_pos_init
moves = 0
crash_df = pd.DataFrame(columns=['cart', 'pos', 'pos_complex', 'next_int'])

# Sorting cart positions to ensure correct processing order (top-to-bottom, left-to-right)
# cart_pos = cart_pos.sort_values(by=['pos_complex'])
crash = False
while crash is False:
    # Move all carts in the correct order
    moves += 1
    for no in range(len(cart_pos)):
        cart_grid, cart_pos = move_cart(cart_grid, cart_pos, no, cart_path)

        # To print each grid after each move
        # for row in cart_grid:
        #     print(row)

        # Check for crashes after all carts have moved
        crash, crash_coords = check_crash(cart_pos)
        if crash:
            break


print('--------------Part 1---------------')
# print(f"\nNew Cart Positions After {moves} Moves:")
# print(cart_pos)

print(f"Crash detected at coordinates: {crash_coords}")
