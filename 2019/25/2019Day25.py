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
        self.game_console = Intcode_CPU(program, debug = False)
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

    def run_console(self, game_input: list[int], visualize: bool) -> list[str]:
        console = self.game_console.replicate()
        console.process_program(game_input)
        output = console.get_result("output")
        screen = self.show_console(output, visualize)
        return screen

    def bruteforced_solution(self, visualize: bool = False):
        spool_cat6 = "north\nwest\nwest\ntake spool of cat6\neast\neast\nsouth\n"
        jam = "east\nnorth\nwest\nnorth\ntake jam\nsouth\neast\nsouth\nwest\n"
        sand = "east\nnorth\ntake sand\nsouth\nwest\n"
        fuel_cell = "east\nnorth\nwest\nwest\nsouth\nwest\ntake fuel cell\neast\nnorth\neast\neast\nsouth\nwest\n"
        checkpoint = "east\nnorth\nwest\nwest\nnorth\nwest\nsouth\n"

        console = self.game_console
        command_list = [
                        sand, jam, spool_cat6, fuel_cell, checkpoint, "inv\n"
                    ]
        game_input = [ord(chr) for command in command_list for chr in list(command)]
        screen = self.run_console(game_input, visualize)
        return re.search(r"\d+", screen[-1]).group()

    def parse_screen(self, screen_lines: list[str]):
        room = ""
        directions = []
        items = []
        parsing = None
        for line in screen_lines:
            if line.startswith("=="):
                room = line.strip("= ").strip()
            elif line == "Doors here lead:":
                parsing = "dirs"
            elif line == "Items here:":
                parsing = "items"
            elif line.startswith("- "):
                if parsing == "dirs":
                    directions.append(line[2:])
                elif parsing == "items":
                    items.append(line[2:])
            elif line == "":
                parsing = None
        return room, directions, items

    def __get_instructions(self, screen_output: list[str]) -> str:
        room, directions, items = self.parse_screen(screen_output)
        avoid_picking = ["infinite loop", "giant electromagnet", "photons", "escape pod", "molten lava"]
        self.rooms_visited.add(room)
        if items not in avoid_picking:
            take_item = f"take {items}"
        print(room, directions, items)
        return f"{directions[0]}\n"

    def automatic_playthrough(self, visualize: bool = False):
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
        spool_cat6 = "north\nwest\nwest\ntake spool of cat6\neast\neast\nsouth\n"
        jam = "east\nnorth\nwest\nnorth\ntake jam\nsouth\neast\nsouth\nwest\n"
        coin = "east\nnorth\nwest\ntake coin\neast\nsouth\nwest\n"
        planetoid = "north\nwest\ntake planetoid\neast\nsouth\n"
        sand = "east\nnorth\ntake sand\nsouth\nwest\n"
        dark_matter = "west\nnorth\ntake dark matter\nsouth\neast\n"
        wreath = "east\nnorth\nwest\nwest\nsouth\ntake wreath\nnorth\neast\neast\nsouth\nwest\n"
        fuel_cell = "east\nnorth\nwest\nwest\nsouth\nwest\ntake fuel cell\neast\nnorth\neast\neast\nsouth\nwest\n"
        electromagnet = "east\nnorth\neast\ntake giant electromagnet\n"
        photons = "west\nsouth\neast\ntake photons\n"
        escape_pod = "east\ntake escape pod\n"
        infinite_loop = "east\nnorth\nwest\nwest\ntake infinite loop\n"
        molten_lava = "east\nnorth\nwest\nwest\nnorth\ntake molten lava\n"
        checkpoint = "east\nnorth\nwest\nwest\nnorth\nwest\nsouth\n"

        reverse_directions = {"north":"south", "south":"north", "east":"west", "west":"east"}
        avoid_picking = ["infinite loop", "giant electromagnet", "photons", "escape pod", "molten lava"]
        command_list = []
        self.rooms_visited = set()
        self.inventory = {}
        iters = 0

        console = self.game_console
        while True:
            iters += 1
            game_input = [ord(chr) for command in command_list for chr in list(command)]
            screen = self.run_console(game_input, visualize)
            next_instruction = self.__get_instructions(screen)
            command_list.append(next_instruction)

            if iters == 4:
                print(command_list)
                break
        return screen[-1]


text_game = Intcode_TextGame(input_program)
# test_play = text_game.automatic_playthrough(True)

password = text_game.bruteforced_solution()
print("Password:", password)

print(f"Execution Time = {time.time() - start_time:.5f}s")
