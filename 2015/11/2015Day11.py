# Advent of Code - Day 11, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/11
# Solution by: [abbasmoosajee07]
# Brief: [Identify and Validate Passwords]

import os

def is_valid(password):
    # Check for forbidden characters [ i, o, l]
    if any(c in password for c in 'iol'):
        return False

    # Check for at least one increasing straight of at least three letters eg,: abc, xyz
    has_straight = any(ord(password[i]) + 
                       1 == ord(password[i + 1]) == ord(password[i + 2]) - 1 
                       for i in range(len(password) - 2))

    if not has_straight:
        return False

    # Check for at least two different pairs of letters eg: aa, bb
    pairs = {}
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            pairs[password[i]] = pairs.get(password[i], 0) + 1

    return len(pairs) >= 2


def increment_password(password):
    password = list(password)
    for i in range(len(password) - 1, -1, -1):
        if password[i] == 'z':
            password[i] = 'a'
        else:
            password[i] = chr(ord(password[i]) + 1)
            break
    return ''.join(password)


def get_next_password(password):
    password = increment_password(password)
    while not is_valid(password):
        password = increment_password(password)
    return password


# Example usage:

D11_file = 'Day11_input.txt'
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

with open(D11_file_path) as file:
   input_data = file.read()

old_password = input_data
new_password_1 = get_next_password(old_password)
new_password_2 = get_next_password(new_password_1)
print("Orignal password :", old_password)
print("First New valid password :", new_password_1)
print("Second New valid password :", new_password_2)

