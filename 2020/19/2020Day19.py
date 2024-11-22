# Advent of Code - Day 19, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/19
# Solution by: [abbasmoosajee07]
# Brief: [Regex and message rules]

#!/usr/bin/env python3

import os, re, copy,regex
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    rules_section, messages_section = file.read().strip().split('\n\n')
    rules = dict(rule.replace('"', '').split(': ', 1) for rule in rules_section.split('\n'))
    messages = messages_section.split('\n')

def expand_rule(rule_id, rules):
    """Recursively expands a rule into a regular expression."""
    rule = rules[rule_id]
    if rule.isalpha():
        return rule  # Direct match for 'a' or 'b'
    return "(?:" + "".join(expand_rule(part, rules) if part.isdigit() else part for part in rule.split()) + ")"

def solve(rules, messages):
    """Counts how many messages match rule 0."""
    regex_pattern = regex.compile(expand_rule("0", rules))
    return sum(bool(regex_pattern.fullmatch(message)) for message in messages)


# Part 1: Count matches with the original rules
part1_result = solve(rules, messages)
print(f"Part 1: {part1_result}")

# Part 2: Modify rules 8 and 11 for recursive matching
rules["8"] = "42 +"
rules["11"] = "(?P<R> 42 (?&R)? 31 )"

part2_result = solve(rules, messages)
print(f"Part 2: {part2_result}")
