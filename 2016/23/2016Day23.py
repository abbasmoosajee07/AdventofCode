# Advent of Code - Day 23, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/23
# Solution by: [abbasmoosajee07]
# Brief: [Register computing variation]
# 
import os

D23_file = 'Day23_input.txt'
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read input file
with open(D23_file_path) as file:
    input_lines = file.read().splitlines()

def get_value(arg, registers):
    # Helper to retrieve either register value or a direct integer
    return registers[arg] if arg in registers else int(arg)

def toggle_instruction(instruction):
    # Split the instruction into parts for easy handling
    parts = instruction.split()
    
    # Toggle based on number of arguments
    if len(parts) == 2:
        if parts[0] == "inc":
            return f"dec {parts[1]}"
        else:
            return f"inc {parts[1]}"
    elif len(parts) == 3:
        if parts[0] == "jnz":
            return f"cpy {parts[1]} {parts[2]}"
        else:
            return f"jnz {parts[1]} {parts[2]}"
    return instruction  # Return unchanged if it's not toggleable

def program(assembly, reg_a, reg_b, reg_c, reg_d):
    counter = 0
    registers = {"a": reg_a, "b": reg_b, "c": reg_c, "d": reg_d}

    while counter < len(assembly):
        instructions = assembly[counter].split()

        # Peephole optimization for loops that behave like multiplication
        if (counter + 5 < len(assembly) and
            assembly[counter].startswith("cpy") and
            assembly[counter + 1].startswith("inc") and
            assembly[counter + 2].startswith("dec") and
            assembly[counter + 3].startswith("jnz") and
            assembly[counter + 4].startswith("dec") and
            assembly[counter + 5].startswith("jnz")):
            
            src = instructions[1]
            inc_reg = assembly[counter + 1].split()[1]
            dec1_reg = assembly[counter + 2].split()[1]
            dec2_reg = assembly[counter + 4].split()[1]

            # Multiply the value in dec2_reg by src and add to inc_reg
            multiplier = get_value(dec2_reg, registers)
            add_value = get_value(src, registers)
            registers[inc_reg] += add_value * multiplier

            # Set both decrementing registers to 0
            registers[dec1_reg] = 0
            registers[dec2_reg] = 0

            counter += 6
            continue

        # Handle the instructions based on their operation
        if instructions[0] == "cpy":
            x = get_value(instructions[1], registers)
            if instructions[2] in registers:
                registers[instructions[2]] = x
            counter += 1

        elif instructions[0] == "tgl":
            x = get_value(instructions[1], registers)
            target_index = counter + x
            if 0 <= target_index < len(assembly):
                assembly[target_index] = toggle_instruction(assembly[target_index])
            counter += 1

        elif instructions[0] == "inc":
            registers[instructions[1]] += 1
            counter += 1

        elif instructions[0] == "dec":
            registers[instructions[1]] -= 1
            counter += 1

        elif instructions[0] == "jnz":
            x = get_value(instructions[1], registers)
            y = get_value(instructions[2], registers)
            if x != 0:
                counter += y
            else:
                counter += 1

        else:
            counter += 1

    reg_a = registers["a"]
    reg_b = registers["b"]
    reg_c = registers["c"]
    reg_d = registers["d"]
    # Return the final state of the registers
    return reg_a, reg_b, reg_c, reg_d

# Part 1
print(f"----------------Part 1----------------")           
a1, b1, c1, d1 = program(input_lines[:], 7, 0, 0, 0)
print(f"When it's all done, the value in a1 = {a1}")
print(f"When it's all done, the value in b1 = {b1}")
print(f"When it's all done, the value in c1 = {c1}")
print(f"When it's all done, the value in d1 = {d1}")

# Part 2
print(f"----------------Part 2----------------")           
a2, b2, c2, d2 = program(input_lines[:], 12, 0, 0, 0)
print(f"When it's all done, the value in a2 = {a2}")
print(f"When it's all done, the value in b2 = {b2}")
print(f"When it's all done, the value in c2 = {c2}")
print(f"When it's all done, the value in d2 = {d2}")
