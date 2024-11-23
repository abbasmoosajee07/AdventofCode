# Advent of Code - Day 10, Year 2024
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2024/day/10
# Solution by: [abbasmoosajee07]
# Brief: [Bracket Matching and Syntax Error Scoring]

#!/usr/bin/env python3
import os

# Define opening and closing characters for brackets
opening = ["{", "[", "(", "<"]
closing = ["}", "]", ")", ">"]

def check_char(chars, index):
    """Recursively checks the characters in the line to find matching brackets."""
    if index >= len(chars):
        return '', 0
    
    char = chars[index]
    char_index = index
    error_message = ""

    while index < len(chars):
        next_char = ""
        
        # If the current character is an opening bracket, check further characters
        if char in opening:
            next_char, current_index = check_char(chars, index + 1)
            
            # If no error, add the corresponding closing bracket
            if current_index == 0:
                if char == "{":
                    next_char += "}"
                elif char == "[":
                    next_char += "]"
                elif char == "(":
                    next_char += ")"
                elif char == "<":
                    next_char += ">"
                return next_char, 0
        
        # If the current character is a closing bracket, return the error
        elif char in closing:
            return char, index
        
        # Continue checking if the next character is a period ('.')
        if next_char == '.':
            index = current_index
            continue
        
        # Handle mismatched brackets
        if char == "{" and next_char != "}":
            error_message = f"Expected }} but found {next_char}"
        elif char == "[" and next_char != "]":
            error_message = f"Expected ] but found {next_char}"
        elif char == "(" and next_char != ")":
            error_message = f"Expected ) but found {next_char}"
        elif char == "<" and next_char != ">":
            error_message = f"Expected > but found {next_char}"
        
        # Raise an exception if there's a mismatch
        if error_message:
            raise Exception(error_message, next_char)
        
        # Continue checking if the current index is at the start of the string
        if char_index == 0 and index < len(chars):
            return check_char(chars, index + 2)
        
        return '.', index + 1

def calculate_syntax_error_score(data):
    """Calculates the syntax error score for the given data."""
    illegal_chars = []
    completed_lines = []

    for line in data:
        try:
            complete, _ = check_char(line, 0)
            completed_lines.append(line + "-" + complete)
        except Exception as error:
            if "Expected" in error.args[0]:
                illegal_chars.append(error.args[1])

    # Calculate the total error score based on the illegal characters
    error_score = 0
    for char in illegal_chars:
        if char == ")":
            error_score += 3
        elif char == "]":
            error_score += 57
        elif char == "}":
            error_score += 1197
        elif char == ">":
            error_score += 25137
    
    return error_score, completed_lines

def calculate_completion_score(completed_lines):
    """Calculates the completion score based on the completed lines."""
    scores = []

    for line in [line.split("-")[1] for line in completed_lines if "-" in line]:
        score = 0
        for char in line:
            score = score * 5
            if char == ")":
                score += 1
            elif char == "]":
                score += 2
            elif char == "}":
                score += 3
            elif char == ">":
                score += 4
        scores.append(score)

    scores.sort()
    return scores[len(scores) // 2]

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read the input data into a list of lines
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')

# Part 1: Calculate the total syntax error score
syntax_error_score, completed_lines = calculate_syntax_error_score(input_data)
print("Part 1:", syntax_error_score)

# Part 2: Calculate the middle completion score
completion_score = calculate_completion_score(completed_lines)
print("Part 2:", completion_score)  # Output should match the expected result for the example
