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
        self.software = software.copy()
        if quarters != 0:
            self.software[0] = quarters  # Set position 0 to 2 for free play

        from Intcode_Computer import Intcode_CPU
        self.console = Intcode_CPU(self.software)

    def run_console(self, joystick_input=None):
        self.console.process_program(external_input=joystick_input)
        output = self.console.get_result('output')
        tile_dict = {(output[i], output[i + 1]): output[i + 2] \
                     for i in range(0, len(output), 3)}
        return tile_dict

    def play_game(self, show_screen: bool = False, play_manually: bool = False):
        """
        Plays the Intcode arcade breakout game and returns the final score using arrow keys for control.
        Pauses after each input.
        Stops the game when the ball goes below the paddle.
        """
        score, ball_x, ball_y, paddle_x, paddle_y = 0, 0, 0, 0, 0
        joystick_input = 0
        original_tiles = {}

        if play_manually:
            import keyboard   # External library for capturing keyboard events
            show_screen = True
            print("Use Left/Right arrow keys to control the paddle. Press 'Esc' to quit.")

        while self.console.running:
            tile_updates = self.run_console(joystick_input)

            for (x, y), tile_id in tile_updates.items():
                if (x, y) == (-1, 0):
                    score = tile_id
                elif tile_id == 3:  # Paddle position
                    paddle_x, paddle_y = x, y
                elif tile_id == 4:  # Ball position
                    ball_x, ball_y = x, y

            if show_screen:
                original_tiles.update(tile_updates)
                self.show_console(original_tiles)

            # Check if ball is below paddle (game over condition)
            if ball_y >= paddle_y:
                print("Game Over! The ball went below the paddle.")
                print(f"Final Score: {score}")
                break
            if play_manually:
                # Pause and capture keyboard input for joystick control
                joystick_input = self.get_joystick_input()
            else:
                # Determine joystick input based on paddle and ball positions
                if ball_x < paddle_x:
                    joystick_input = -1  # Move paddle left
                elif ball_x > paddle_x:
                    joystick_input = +1  # Move paddle right
                else:
                    joystick_input =  0  # Stay neutral

            self.console.output_list = []
            self.console.paused = False

        return score

    def get_joystick_input(self):
        """
        Waits for a key press and returns the corresponding joystick input.
        """
        import keyboard   # External library for capturing keyboard events

        while True:
            event = keyboard.read_event()  # Wait for key press
            if event.event_type == keyboard.KEY_DOWN:  # Ensure key is pressed down
                if event.name == 'left':
                    return -1  # Move paddle left
                elif event.name == 'right':
                    return 1  # Move paddle right
                elif event.name == 'esc':
                    print("Game exited.")
                    exit()  # Exit the game if Esc is pressed
                else:
                    return 0  # Neutral if no arrow key is pressed

    def show_console(self, tiles: dict):
        TILE_DICT = {0: ' ', 1: '#', 2: '=', 3: 'T', 4: 'O'}

        min_x = min(x for x, _ in tiles.keys())
        max_x = max(x for x, _ in tiles.keys())
        min_y = min(y for _, y in tiles.keys())
        max_y = max(y for _, y in tiles.keys())

        tiles_grid = []
        for y in range(min_y, max_y + 1):
            row = ''
            for x in range(min_x, max_x + 1):
                tile_id = tiles.get((x, y), 0)
                row += TILE_DICT.get(tile_id, ' ')
            tiles_grid.append(row)

        print("Score:", tiles.get((-1, 0), 0))
        print("\n".join(tiles_grid))
        print("\n" + "." * 40)

# Initialize and play the game
arcade_p1 = Intcode_Arcade(input_program)
exit_tiles = arcade_p1.run_console()
block_count = sum(1 for tile in exit_tiles.values() if tile == 2)
print("Part 1:", block_count)

arcade_p2 = Intcode_Arcade(input_program, quarters=2)
final_score = arcade_p2.play_game()
print("Part 2:", final_score)

# print(f"Execution Time = {time.time() - start_time:.5f}s")
