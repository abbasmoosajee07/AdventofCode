# Advent of Code - Day 23, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/23
# Solution by: [abbasmoosajee07]
# Brief: [Register Computing]

import os

D23_file = 'Day23_input.txt'
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

with open(D23_file_path) as file:
    instruc_list = file.read()
    
instruc_list = instruc_list.splitlines()
# print(instruc_list)



def program(assembly, reg_a, reg_b):
    counter = 0
    while counter < len(assembly):
        instructions = assembly[counter].split()
        if len(instructions) == 2:
            
            # hlf r sets reg r to half its current value, then continues with the next instruction.
            if instructions[0] == "hlf":
                if instructions[1] == "a":
                    reg_a = reg_a / 2
                else:
                    reg_b = reg_b / 2
                counter += 1
                
            # tpl r sets reg r to triple its current value, then continues with the next instruction.
            elif instructions[0] == "tpl":
                if instructions[1] == "a":
                    reg_a *= 3
                else:
                    reg_b *= 3
                counter += 1
                
            # inc r increments reg r, adding 1 to it, then continues with the next instruction.
            elif instructions[0] == "inc":
                if instructions[1] == "a":
                    reg_a += 1
                else:
                    reg_b += 1
                counter += 1
                
            # jmp offset is a jump; it continues with the instruction offset away relative to itself.
            elif instructions[0] == "jmp":
                counter += int(instructions[1])
        elif len(instructions) == 3:
            
            # jie r, offset is like jmp, but only jumps if reg r is even ("jump if even").
            if instructions[0] == "jie":
                if instructions[1].strip(',') == "a":
                    if reg_a % 2 == 0:
                        counter += int(instructions[2])
                    else:
                        counter += 1
                else:
                    if reg_b % 2 == 0:
                        counter += int(instructions[2])
                    else:
                        counter += 1
                        
            # jio r, offset is like jmp, but only jumps if reg r is 1 ("jump if one", not odd).            
            elif instructions[0] == "jio":
                if instructions[1].strip(',') == "a":
                    if reg_a == 1:
                        counter += int(instructions[2])
                    else:
                        counter += 1
                else:
                    if reg_b == 1:
                        counter += int(instructions[2])
                    else:
                        counter += 1
    
    return reg_a, reg_b
                    
a1, b1 = program(instruc_list, 0, 0) 
print(f"----------------Part 1----------------")           
print(f"When it's all done, the value in {a1 = }")
print(f"When it's all done, the value in {b1 = }")

a2, b2 = program(instruc_list, 1, 0)            
print(f"----------------Part 2----------------")           
print(f"When it's all done, the value in {a2 = }")
print(f"When it's all done, the value in {b2 = }")