# Advent of Code - Day 12, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/12
# Solution by: [abbasmoosajee07]
# Brief: [Registry computing]

import os

D12_file = 'Day12_input.txt'
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read input file
with open(D12_file_path) as file:
    input_lines = file.read().splitlines()
# print(input_lines)

def get_value(val, reg_a, reg_b, reg_c, reg_d):
    if val == "a":
        return reg_a
    elif val == "b":
        return reg_b
    elif val == "c":
        return reg_c
    elif val == "d":
        return reg_d
    else:
        return int(val)

def program(assembly, reg_a, reg_b, reg_c, reg_d):
    counter = 0
    while counter < len(assembly):
        instructions = assembly[counter].split()
        # cpy x y copies x (either an integer or the value of a register) into register y.
        if instructions[0] == "cpy":
            
            if instructions[1] == "a":
                x = reg_a
            elif instructions[1] == "b":
                x = reg_b
            elif instructions[1] == "c":
                x = reg_c
            elif instructions[1] == "d":
                x = reg_d
            else:
                x = int(instructions[1])

            if instructions[2] == "a":
                reg_a = x
            elif instructions[2] == "b":
                reg_b = x
            elif instructions[2] == "c":
                reg_c = x
            elif instructions[2] == "d":
                reg_d = x
            counter += 1
        
        # inc x increases the value of register x by one.
        elif instructions[0] == "inc":
            if instructions[1] == "a":
                reg_a += 1
            elif instructions[1] == "b":
                reg_b += 1
            elif instructions[1] == "c":
                reg_c += 1
            elif instructions[1] == "d":
                reg_d += 1
            counter += 1
    
        # dec x decreases the value of register x by one.       
        elif instructions[0] == "dec":
            if instructions[1] == "a":
                reg_a -= 1
            elif instructions[1] == "b":
                reg_b -= 1
            elif instructions[1] == "c":
                reg_c -= 1
            elif instructions[1] == "d":
                reg_d -= 1
            counter += 1

        # jnz x y jumps to an instruction y away (positive means forward; 
        #         negative means backward), but only if x is not zero.
        elif instructions[0] == "jnz":
            x = get_value(instructions[1], reg_a, reg_b, reg_c, reg_d)
            if x != 0:
                counter += int(instructions[2])
            else:
                counter += 1

    return reg_a, reg_b, reg_c, reg_d

print(f"----------------Part 1----------------")           
a1, b1, c1, d1 = program(input_lines, 0, 0, 0, 0)
print(f"When it's all done, the value in a1 = {a1}")
print(f"When it's all done, the value in b1 = {b1}")
print(f"When it's all done, the value in c1 = {c1}")
print(f"When it's all done, the value in d1 = {d1}")

print(f"----------------Part 2----------------")           
a2, b2, c2, d2 = program(input_lines, 0, 0, 1, 0)
print(f"When it's all done, the value in a2 = {a2}")
print(f"When it's all done, the value in b2 = {b2}")
print(f"When it's all done, the value in c2 = {c2}")
print(f"When it's all done, the value in d2 = {d2}")
