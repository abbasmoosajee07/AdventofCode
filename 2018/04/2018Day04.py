# Advent of Code - Day 4, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/4
# Solution by: [abbasmoosajee07]
# Brief: [Guard Shifts]

import os
import collections
from datetime import datetime
import dateutil.parser

# Load the input data from the specified file path
D4_file = "Day04_input.txt"
D4_file_path =  os.path.join(os.path.dirname(os.path.abspath(__file__)),D4_file)  # Updated path for better compatibility

# Read and sort input data for chronological order
with open(D4_file_path) as file:
    input_data = file.read().strip().splitlines()
    input_data.sort()  # Sort entries by date and time order
# print(input_data)

# Load the input data from the specified file path
def load_input(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path) as file:
        data = file.read().strip().splitlines()
    return sorted(data)

# Parse each line into timestamp and action, and organize sleep data by guard
def parse_guard_data(input_data):
    guards = collections.defaultdict(list)  # Tracks sleep intervals for each guard
    times = collections.defaultdict(int)    # Tracks total sleep time for each guard
    guard = None
    start = None

    for line in input_data:
        time, action = line.split('] ')     # Split into timestamp and action
        time = dateutil.parser.parse(time[1:])  # Parse timestamp into datetime object

        if action.startswith('Guard'):
            guard = int(action.split()[1][1:])  # Extract guard ID
        elif action == 'falls asleep':
            start = time.minute                 # Record sleep start minute
        elif action == 'wakes up' and guard is not None and start is not None:
            end = time.minute                   # Record wake-up minute
            guards[guard].append((start, end))  # Track sleep interval
            times[guard] += end - start         # Accumulate total sleep time

    return guards, times

# Identify the guard with the most total sleep time and the minute most frequently asleep
def find_sleepiest_guard(guards, times):
    guard, _ = max(times.items(), key=lambda x: x[1])  # Guard with most sleep time
    minute, _ = max(
        ((minute, sum(1 for start, end in guards[guard] if start <= minute < end))
         for minute in range(60)), key=lambda x: x[1]
    )
    return guard, minute

# Find the guard most frequently asleep on any specific minute
def find_most_frequent_minute(guards):
    guard, minute, _ = max(
        ((guard, minute, sum(1 for start, end in guards[guard] if start <= minute < end))
         for minute in range(60) for guard in guards), key=lambda x: x[2]
    )
    return guard, minute

guards, times = parse_guard_data(input_data)

# Part 1: Calculate result for guard with most sleep time on any minute
guard, minute = find_sleepiest_guard(guards, times)
print(f"Part 1: Sleepiest Guard Value is {guard * minute}")

# Part 2: Calculate result for guard most frequently asleep on a specific minute
guard, minute = find_most_frequent_minute(guards)
print(f"Part 2: Most frequent minute is {guard * minute}")

