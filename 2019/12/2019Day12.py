# Advent of Code - Day 12, Year 2019
# Solution Started: Nov 19, 2024
# Puzzle Link: https://adventofcode.com/2019/day/12
# Solution by: [abbasmoosajee07]
# Brief: [Modelling Jupyter's Moons]

#!/usr/bin/env python3

import os, re, time
from itertools import combinations, count
from math import gcd
from functools import reduce

class Moon:
    def __init__(self, position):
        self.position = list(position)
        self.velocity = [0, 0, 0]

    def total_energy(self):
        potential_energy = sum(abs(x) for x in self.position)
        kinetic_energy = sum(abs(x) for x in self.velocity)
        return potential_energy * kinetic_energy

class MoonSystem:
    def __init__(self, moon_positions):
        self.moons = [Moon(position) for position in moon_positions]

    def apply_gravity(self, dim):
        for A, B in combinations(self.moons, 2):
            if A.position[dim] < B.position[dim]:
                A.velocity[dim] += 1
                B.velocity[dim] -= 1
            elif A.position[dim] > B.position[dim]:
                A.velocity[dim] -= 1
                B.velocity[dim] += 1

    def apply_velocity(self, dim):
        for moon in self.moons:
            moon.position[dim] += moon.velocity[dim]

    def get_state(self, dim):
        """Get the state for a specific dimension as a tuple of positions and velocities."""
        return tuple((moon.position[dim], moon.velocity[dim]) for moon in self.moons)

    def simulate(self, steps):
        for _ in range(steps):
            for dim in range(3):
                self.apply_gravity(dim)
                self.apply_velocity(dim)

    def total_energy(self):
        return sum(moon.total_energy() for moon in self.moons)

    def find_cycle_lengths(self):
        initial_states = [self.get_state(dim) for dim in range(3)]
        cycle_lengths = [0] * 3

        for dim in range(3):
            for step in count(1):
                self.apply_gravity(dim)
                self.apply_velocity(dim)

                if self.get_state(dim) == initial_states[dim]:
                    cycle_lengths[dim] = step
                    break

        return cycle_lengths

def parse_input(filepath):
    """Parse the input file to extract moon positions."""
    with open(filepath) as file:
        return [[int(value) for value in re.findall(r'-?\d+', line)] for line in file]

# Utility to calculate LCM
def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def lcm_multiple(numbers):
    return reduce(lcm, numbers)

start_time = time.time()

# File input path setup
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Parse input data
moon_positions = parse_input(D12_file_path)
system = MoonSystem(moon_positions)

# Part 1: Simulate for 1000 steps and calculate total energy
system.simulate(1000)
part1_result = system.total_energy()
print(f"Part 1: {part1_result}")

# Part 2: Find the steps to the first repeated state
system = MoonSystem(moon_positions)  # Reset the system for Part 2
cycle_lengths = system.find_cycle_lengths()
part2_result = lcm_multiple(cycle_lengths)
print(f"Part 2: {part2_result}")

print(f"Execution Time = {time.time() - start_time:.5f}s")
