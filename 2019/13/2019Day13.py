# Advent of Code - Day 13, Year 2019
# Solution Started: Jan 24, 2025
# Puzzle Link: https://adventofcode.com/2019/day/13
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Arcade Game]

#!/usr/bin/env python3

import os, sys, copy, time
start_time = time.time()

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)
# from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

# Read and parse input data
with open(D13_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Arcade:
    """
    Simulates the Breakout Arcade game based on where the brains of the computer is the Intcode CPU
    """
    def __init__(self, software: list[int], quarters: int = 0):
        """
        Initialize the arcade with the given software and set the game mode.
        """
        # Modify the software to enable free play
        self.software = software.copy()
        if quarters != 0:
            self.software[0] = quarters  # Set position 0 to 2 for free play

        from Intcode_Computer import Intcode_CPU
        self.console = Intcode_CPU(self.software)

    def run_console(self, joystick_input = None):
        """
        Runs the Intcode program and retrieves the tile updates.
        """
        self.console.process_program(external_input=joystick_input)

        # Process outputs in batches of three
        output = self.console.get_result('output')
        tile_dict = {(output[i], output[i + 1]): output[i + 2] \
                        for i in range(0, len(output), 3)}
        return tile_dict

    def play_game(self, show_screen: bool = False):
        """
        Plays the Intcode arcade breakout game and returns the final score.
        """
        # Initialize the game state
        score, ball_x, paddle_x = 0, 0, 0
        joystick_input = None
        original_tiles = {}

        # Play the game on the arcade console
        while self.console.running:

            tile_updates = self.run_console(joystick_input)

            for (x, y), tile_id in tile_updates.items():
                if (x, y) == (-1, 0):
                    score = tile_id  # Update the score
                elif tile_id == 3:  # Paddle position
                    paddle_x = x
                elif tile_id == 4:  # Ball position
                    ball_x = x

            # Determine joystick input based on paddle and ball positions
            if ball_x < paddle_x:
                joystick_input = -1  # Move paddle left
            elif ball_x > paddle_x:
                joystick_input = +1  # Move paddle right
            else:
                joystick_input =  0  # Stay neutral

            # Clear the output buffer and unpause console
            self.console.output_list = []
            self.console.paused = False

            # Show the game screen if enabled
            if show_screen:
                # Update the original tiles dictionary and show console
                original_tiles.update(tile_updates)
                self.show_console(original_tiles)

        return score

    def show_console(self, tiles: dict):
        """
        Displays the current state of the arcade game grid.
        """
        TILE_DICT = {0: '  ', 1: ' #', 2: '==', 3: '__', 4: '()'}  # Tile representations

        # Determine the bounds of the grid
        min_x = min(x for x, _ in tiles.keys())
        max_x = max(x for x, _ in tiles.keys())
        min_y = min(y for _, y in tiles.keys())
        max_y = max(y for _, y in tiles.keys())

        # Create the grid and print it
        tiles_grid = []
        for y in range(min_y, max_y + 1):  # Loop over rows (y-coordinates)
            row = ''
            for x in range(min_x, max_x + 1):  # Loop over columns (x-coordinates)
                tile_id = tiles.get((x, y), 0)  # Default to empty space
                row += TILE_DICT.get(tile_id, ' ')  # Map tile_id to its visual representation
            tiles_grid.append(row)

        # Print the grid row by row
        print("Score:", tiles.get((-1, 0), 0))
        print("\n".join(tiles_grid))
        print("\n" + "." * 40)  # Separator for each game frame

# Initialize and play the game
arcade_p1 = Intcode_Arcade(input_program)
exit_tiles = arcade_p1.run_console()
block_count = sum(1 for tile in exit_tiles.values() if tile == 2)
print("Part 1:", block_count)

arcade_p2 = Intcode_Arcade(input_program, quarters=2)
final_score = arcade_p2.play_game()
print("Part 2:", final_score)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
