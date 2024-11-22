# Advent of Code - Day 16, Year 2020
# Solution Started: Nov 21, 2024
# Puzzle Link: https://adventofcode.com/2020/day/16
# Solution by: [abbasmoosajee07]
# Brief: [Filling missing information]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Parse input data into sections
with open(D16_file_path) as file:
    input_data = file.read().strip().split('\n\n')


# Parsing Functions
def parse_rules(rules_section):
    rules = {}
    for line in rules_section.split('\n'):
        name, ranges = line.split(': ')
        range1, range2 = ranges.split(' or ')
        r1_start, r1_end = map(int, range1.split('-'))
        r2_start, r2_end = map(int, range2.split('-'))
        rules[name] = [(r1_start, r1_end), (r2_start, r2_end)]
    return rules


def parse_tickets(ticket_section):
    return [list(map(int, line.split(','))) for line in ticket_section.split('\n')[1:]]


# Parse all input sections
rules = parse_rules(input_data[0])
your_ticket = parse_tickets(input_data[1])[0]
nearby_tickets = parse_tickets(input_data[2])


# Part 1: Finding invalid tickets
def is_valid_for_any_rule(number, rules):
    for ranges in rules.values():
        for r_start, r_end in ranges:
            if r_start <= number <= r_end:
                return True
    return False


def find_invalid_tickets(tickets, rules):
    invalid_numbers = []
    valid_tickets = []
    for ticket in tickets:
        ticket_valid = True
        for number in ticket:
            if not is_valid_for_any_rule(number, rules):
                invalid_numbers.append(number)
                ticket_valid = False
        if ticket_valid:
            valid_tickets.append(ticket)
    return invalid_numbers, valid_tickets


invalid_numbers, valid_tickets = find_invalid_tickets(nearby_tickets, rules)
print("Part 1:", sum(invalid_numbers))


# Part 2: Identifying field mappings
def find_field_mapping(tickets, rules):
    field_candidates = {field: set(range(len(tickets[0]))) for field in rules}
    
    for ticket in tickets:
        for idx, value in enumerate(ticket):
            for field, ranges in rules.items():
                if not any(r_start <= value <= r_end for r_start, r_end in ranges):
                    field_candidates[field].discard(idx)
    
    field_mapping = {}
    while field_candidates:
        for field, candidates in list(field_candidates.items()):
            if len(candidates) == 1:
                idx = candidates.pop()
                field_mapping[field] = idx
                del field_candidates[field]
                for remaining_candidates in field_candidates.values():
                    remaining_candidates.discard(idx)
    return field_mapping


field_mapping = find_field_mapping(valid_tickets, rules)

# Calculate the product of "departure" fields on your ticket
departure_product = 1
for field, idx in field_mapping.items():
    if field.startswith("departure"):
        departure_product *= your_ticket[idx]

print("Part 2:", departure_product)
