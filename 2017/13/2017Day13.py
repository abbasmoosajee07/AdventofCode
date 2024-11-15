# Advent of Code - Day 13, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/13
# Solution by: [abbasmoosajee07]
# Brief: [Breaking Firewalls]


import os, re, copy

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

with open(D13_file_path) as file:
    input_data = file.read().strip().split("\n")


def parse_firewall(firewall_props):
    """Parses input data to build the firewall with each depth and range."""
    firewall = {}
    for line in firewall_props:
        depth, range_ = map(int, line.split(": "))
        firewall[depth] = range_
    return firewall


def calculate_severity(firewall):
    """Calculates the total severity of getting caught in the firewall."""
    severity = 0
    for depth, range_ in firewall.items():
        # Scanner cycle is 2 * (range - 1), caught if at 0 position
        cycle = 2 * (range_ - 1)
        if depth % cycle == 0:
            severity += depth * range_
    return severity


def find_min_delay(firewall):
    """Finds the minimum delay to pass through the firewall without being caught."""
    delay = 0
    while True:
        caught = False
        for depth, range_ in firewall.items():
            cycle = 2 * (range_ - 1)
            # Check if packet is caught at current delay
            if (depth + delay) % cycle == 0:
                caught = True
                break
        if not caught:
            return delay
        delay += 1


# Part 1: Calculate severity if starting immediately
firewall = parse_firewall(input_data)
part1_result = calculate_severity(firewall)
print("Part 1 Severity:", part1_result)

# Part 2: Find the minimum delay to avoid all scanners
part2_result = find_min_delay(firewall)
print("Part 2 Minimum Delay:", part2_result)
