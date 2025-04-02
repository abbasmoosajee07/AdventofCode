"""Advent of Code - Day 25, Year 2019
Solution Started: Apr 1, 2025
Puzzle Link: https://adventofcode.com/2019/day/25
Solution by: abbasmoosajee07
Brief: [Intcode TextGame]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
start_time = time.time()

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)
# from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

# Read and sort input data into a grid
with open(D25_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_TextGame:
    def __init__(self, program: list[int]):
        from Intcode_Computer import Intcode_CPU
        self.game_console = Intcode_CPU(program)
        self.game_software = program

    @staticmethod
    def show_console(screen_output: list[int], visualize: bool = True)-> list[str]:
        """
        Display the game console screen in the current state.
        """
        screen_grid = ''.join(map(chr, screen_output))
        screen_rows = screen_grid.strip().split('\n')

        if visualize:
            print('\n'.join(screen_rows))
            print("_" * len(screen_rows[0]))

        return screen_rows

    def play_game(self, visualize: bool = False):
        """
        -Movement via north, south, east, or west.
        -To take an item the droid sees in the environment,
            use the command take <name of item>. For example,
            if the droid reports seeing a red ball, you can pick
            it up with take red ball.
        -To drop an item the droid is carrying, use the command
            drop <name of item>. For example, if the droid is
            carrying a green ball, you can drop it with drop green ball.
        -To get a list of all of the items the droid is currently carrying,
            use the command inv (for "inventory").
        """
        dark_matter = "west\nnorth\ntake dark matter\nsouth\neast\n"
        photons = "west\nsouth\neast\ntake photons\n"
        escape_pod = "east\ntake escape pod\n"
        planetoid = "north\nwest\ntake planetoid\neast\nsouth\n"
        spool_cat6 = "north\nwest\nwest\ntake spool of cat6\neast\neast\nsouth\n"
        sand = "east\nnorth\ntake sand\nsouth\nwest\n"
        coin = "east\nnorth\nwest\ntake coin\neast\nsouth\nwest\n"
        jam = "east\nnorth\nwest\nnorth\ntake jam\nsouth\neast\nsouth\nwest\n"
        electromagnet = "east\nnorth\neast\ntake giant electromagnet\n"

        console = self.game_console
        command_list = [dark_matter, planetoid, sand, coin, jam, spool_cat6, photons, escape_pod,
                        "inv\n"
                    ]
        while True:
            console.process_program()
            output = console.get_result("output")
            # screen = self.show_console(output)
            game_input = [ord(chr) for command in command_list for chr in list(command)]
            console.paused = False
            console.process_program(game_input)
            output = console.get_result("output")
            screen = self.show_console(output)
            break
        return screen

text_game = Intcode_TextGame(input_program)
password = text_game.play_game(True)
print("Part 1:", password)

print(f"Execution Time = {time.time() - start_time:.5f}s")
