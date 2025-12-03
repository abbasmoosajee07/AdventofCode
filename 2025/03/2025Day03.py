"""Advent of Code - Day 3, Year 2025
Solution Started: December 3, 2025
Puzzle Link: https://adventofcode.com/2025/day/3
Solution by: Abbas Moosajee
Brief: [Lobby]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "Day03_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

def max_jolts_basic(battery_list):
    max_jolts = []
    for battery in battery_list:
        batteries_avail = list(map(int, list(battery)))
        first_battery = max(batteries_avail[:-1])
        first_idx = batteries_avail.index(first_battery)
        second_battery = max(batteries_avail[first_idx + 1:])
        max_jolts.append(int(f"{first_battery}{second_battery}"))
    return sum(max_jolts)

def maximise_jolts(battery, array_size):
    memory = [0] * (array_size + 1)
    for bat in battery:
        memory = [0] + [
            max(memory[n + 1], memory[n] * 10 + int(bat))
            for n in range(array_size)
        ]
    return memory[array_size]

print("AoC Day 3, P1:", sum(maximise_jolts(battery,  2) for battery in data))
print("AoC Day 3, P2:", sum(maximise_jolts(battery, 12) for battery in data))
