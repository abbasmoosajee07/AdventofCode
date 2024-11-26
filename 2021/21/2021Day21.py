# Advent of Code - Day 21, Year 2021
# Solution Started: Nov 26, 2024
# Puzzle Link: https://adventofcode.com/2021/day/21
# Solution by: [abbasmoosajee07]
# Brief: [Dirac Dice]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
from itertools import product, cycle
from functools import lru_cache

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split('\n')

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_player_info(player_list):
    """Parse the input data to get player starting positions."""
    player_dict = {}
    for player in player_list:
        player_number, start_position = map(int,
                re.search(r"Player (\d+) starting position: (\d+)",
                    player).groups())
        player_dict[player_number] = [start_position, 0]  # [position, score]
    return player_dict

def play_turn(players, player_no, total_rolls, dice_size = 100):
    """Simulate a player's turn by rolling dice and updating their position and score."""
    board_position = players[player_no][0]

    # Roll the dice 3 times per turn
    for _ in range(ROLLS_PER_TURN):
        dice_roll = (total_rolls % dice_size) + 1  # Dice rolls between 1 and 100
        total_rolls += 1  # Move to the next dice roll

        # Update the player's board position with wrap-around
        board_position = (board_position + dice_roll - 1) % BOARD_SIZE + 1

    # Update the player's position and score
    players[player_no][0] = board_position
    players[player_no][1] += board_position  # Add the new board position to score

    return players, total_rolls  # Continue the game otherwise


BOARD_SIZE = 10
ROLLS_PER_TURN = 3

def play_simple_game(player_init, winning_score):
    player_dict = copy.deepcopy(player_init)
    turn = 0
    total_rolls = 0
    game_over = False

    while not game_over:
        # Alternate between player 1 and player 2
        player_no = (turn % len(player_dict)) + 1
        player_dict, total_rolls = play_turn(player_dict, player_no, total_rolls)
        turn += 1
        if player_dict[player_no][1] >= winning_score:
            game_over = True

    losing_player = (player_no % len(player_dict)) + 1
    losing_player_score = player_dict[losing_player][1]
    return total_rolls * losing_player_score

player_init = parse_player_info(input_data)
ans_p1 = play_simple_game(player_init, winning_score = 1000)
print("Part 1:", ans_p1)

# Precompute all possible quantum dice roll outcomes (sums of 3 rolls of a 3-sided die)
QUANTUM_ROLLS = tuple(sum(rolls) for rolls in product(range(1, 4), repeat=3))

@lru_cache(maxsize=None)
def play_quantum_round(current_player_pos, current_player_score, other_player_pos, other_player_score, score_limit):
    """
    Recursively simulate all possible universes for the quantum dice game.
    
    Arguments:
    - current_player_pos: The current position of the active player.
    - current_player_score: The score of the active player.
    - other_player_pos: The current position of the opponent.
    - other_player_score: The score of the opponent.
    - score_limit: The score required to win the game.

    Returns:
    - A tuple (current_player_wins, other_player_wins), representing the number
      of universes won by each player from this state.
    """
    # If the current player has reached or exceeded the score limit, they win
    if current_player_score >= score_limit:
        return 1, 0

    # If the other player has reached or exceeded the score limit, they win
    if other_player_score >= score_limit:
        return 0, 1

    # Track the total wins for both players
    current_player_wins = 0
    other_player_wins = 0

    # Iterate over all possible quantum dice roll outcomes
    for roll_sum in QUANTUM_ROLLS:
        # Calculate the new position and score for the current player
        new_position = (current_player_pos + roll_sum - 1) % 10 + 1
        new_score = current_player_score + new_position

        # Simulate the game from the opponent's perspective (switch turns)
        opponent_wins, player_wins = play_quantum_round(
            other_player_pos, other_player_score, new_position, new_score, score_limit
        )

        # Update the win counts for this branch
        current_player_wins += player_wins
        other_player_wins += opponent_wins

    return current_player_wins, other_player_wins

def start_quantum_game(player_dict, score_limit):

    player_pos_1 = player_dict[1][0]
    player_score_1 = player_dict[1][1]
    player_pos_2 = player_dict[2][0]
    player_score_2 = player_dict[2][1]

    wins =  play_quantum_round(player_pos_1, player_score_1, player_pos_2, player_score_2, score_limit)
    return wins

score_limit = 21
quantum_iters = start_quantum_game(player_init, score_limit)
print("Part 2:", max(quantum_iters))

