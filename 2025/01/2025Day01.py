"""Advent of Code - Day 1, Year 2025
Solution Started: December 1, 2025
Puzzle Link: https://adventofcode.com/2025/day/1
Solution by: Abbas Moosajee
Brief: [Secret Entrance ]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "Day01_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class AOC_Dial:
    def __init__(self, inp_instr):
        self.instructions = [
            (instr[0], int(instr[1:])) for instr in inp_instr
        ]
        self.dial = list(range(0, 100))
    def rotate_dial(self, start_val):
        pointer_val = start_val
        pointer_idx = self.dial.index(start_val)
        pass_zero = 0
        dial_len = len(self.dial)
        for dir, magn in self.instructions:
            if dir == "R":
                shift = 1
            elif dir == "L":
                shift = -1
            pointer_idx = (pointer_idx + (shift * magn)) % dial_len
            pointer_val = self.dial[pointer_idx]
            if pointer_val == 0:
                pass_zero += 1
        return pass_zero


    def rotate_incrementally(self, start_val):
        pointer_idx = self.dial.index(start_val)
        dial_len = len(self.dial)
        pass_zero = 0
        for dir, magn in self.instructions:
            step = 1 if dir == "R" else -1

            for _ in range(magn):
                pointer_idx = (pointer_idx + step) % dial_len
                pointer_val = self.dial[pointer_idx]
                if pointer_val == 0:
                    pass_zero += 1

        return pass_zero


dial_p1 = AOC_Dial(data)
password_p1 = dial_p1.rotate_dial(50)
print("AoC Day 1, P1:", password_p1)

dial_p2 = AOC_Dial(data)
password_p2 = dial_p2.rotate_incrementally(50)
print("AoC Day 1, P2:", password_p2)