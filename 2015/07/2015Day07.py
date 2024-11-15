# Advent of Code - Day 7, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/7
# Solution by: [abbasmoosajee07]
# Brief: [Circuits]

import os
import re
import numpy as np

D7_file = 'Day07_input.txt'
D7_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D7_file)

with open(D7_file_path) as file:
    circuits = file.read()

circuits = circuits.splitlines()

# Parse the instructions and store them
def parse_instructions(instructions):
    wires = {}
    for line in instructions:
        parts = line.split(" -> ")
        wires[parts[1].strip()] = parts[0].strip()
    return wires

# Evaluate the signal of a given wire
def evaluate(wire, wires, cache):
    if wire.isdigit():
        return int(wire)
    
    if wire in cache:
        return cache[wire]
    
    instruction = wires[wire]
    
    if "AND" in instruction:
        x, y = instruction.split(" AND ")
        value = evaluate(x, wires, cache) & evaluate(y, wires, cache)
    elif "OR" in instruction:
        x, y = instruction.split(" OR ")
        value = evaluate(x, wires, cache) | evaluate(y, wires, cache)
    elif "LSHIFT" in instruction:
        x, n = instruction.split(" LSHIFT ")
        value = evaluate(x, wires, cache) << int(n)
    elif "RSHIFT" in instruction:
        x, n = instruction.split(" RSHIFT ")
        value = evaluate(x, wires, cache) >> int(n)
    elif "NOT" in instruction:
        x = instruction.split("NOT ")[1]
        value = ~evaluate(x, wires, cache) & 0xFFFF  # Mask to 16 bits
    else:
        value = evaluate(instruction, wires, cache)
    
    cache[wire] = value
    return value

# Main function to find the signal for wire 'a'
def find_signal(instructions,signal):
    wires = parse_instructions(instructions)
    cache = {}
    return evaluate(signal, wires, cache)

# Part Two: Override wire 'b' and recompute the signal for 'a'
def override_b_and_recompute(instructions, new_value_for_b, signal):
    # Modify the instructions to override wire 'b'
    modified_instructions = instructions.copy()
    for i in range(len(modified_instructions)):
        if " -> b" in modified_instructions[i]:
            modified_instructions[i] = f"{new_value_for_b} -> b"
            break
    
    # Now recompute the signal for 'a' with the new instructions
    return find_signal(modified_instructions, signal)

target_signal = "y"
# Step 1: Get the original signal for 'a' (from part one)
signal_a = find_signal(circuits, target_signal)
print(f"Original signal to wire '{target_signal}': {signal_a}")

# Step 2: Override 'b' with the value of 'a' and recompute 'a'
new_signal_a = override_b_and_recompute(circuits, signal_a, target_signal)
print(f"New signal to wire '{target_signal}': {new_signal_a}")
