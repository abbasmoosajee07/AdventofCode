# Advent of Code - Day 25, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/25
# Solution by: [abbasmoosajee07]
# Brief: [Final Day Puzzle, register computing variation]

# Needs specfic puzzle input to work
import re
import os

# Constants for the assembly program
HEIGHT = 6
WIDTH = 50

# Regex pattern to parse instructions
PARSER = re.compile("(inc|dec|cpy|jnz|tgl|out) (-?\d+|[a-d]) ?(-?\d+|[a-d])?$")

# Function to parse input instructions
def parse_input(input_seq):
    for cmd in input_seq:
        match = PARSER.match(cmd)
        if match:
            op, a, b = match.groups()
            if not a.isalpha():
                a = int(a)
            if b is not None:
                if not b.isalpha():
                    b = int(b)
                yield (op, (a, b))
            else:
                yield (op, (a,))

# Toggling instructions
def tgl(code, registers, value):
    target_index = registers["ip"] + registers.get(value, value)
    if 0 <= target_index < len(code) and target_index != registers["ip"]:
        instr = code[target_index]
        if instr[0] == "inc":
            instr = ("dec",) + instr[1:]
        elif instr[0] in ("dec", "tgl"):
            instr = ("inc",) + instr[1:]
        elif instr[0] == "jnz":
            instr = ("cpy",) + instr[1:]
        elif instr[0] == "cpy":
            instr = ("jnz",) + instr[1:]
        code[target_index] = instr
    registers["ip"] += 1

# Incrementing a register
def inc(code, registers, reg):
    registers[reg] += 1
    registers["ip"] += 1

# Decrementing a register
def dec(code, registers, reg):
    registers[reg] -= 1
    registers["ip"] += 1

# Copying values between registers
def cpy(code, registers, value, reg):
    registers[reg] = registers.get(value, value)
    registers["ip"] += 1

# Jumping if not zero
def jnz(code, registers, value, offset):
    if registers.get(value, value) != 0:
        registers["ip"] += registers.get(offset, offset)
    else:
        registers["ip"] += 1

# Exception for invalid output
class BunnyException(Exception):
    pass

# Output the value and check for validity
def out(code, registers, value):
    val = registers.get(value, value)
    if val not in (1, 0) or (registers["out"] and val == registers["out"][-1]):
        raise BunnyException
    registers["out"].append(val)
    registers["ip"] += 1

# Dictionary of operations
OP = {
    "jnz": jnz,
    "inc": inc,
    "dec": dec,
    "cpy": cpy,
    "tgl": tgl,
    "out": out
}

# Execute the code
def execute(code, stop, **kwargs):
    registers = {"a": 0, "b": 0, "c": 0, "d": 0, "ip": 0, "out": []}
    registers.update(kwargs)
    c = 0
    while registers["ip"] < len(code) and c < stop:
        c += 1
        cmd, args = code[registers["ip"]]
        OP[cmd](code, registers, *args)
    return registers

# Main function to drive the program
def main():
    D25_file = 'Day25_input.txt'
    D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

    with open(D25_file_path) as inp:
        inp_seq = list(inp)
        parsed_input = list(parse_input(inp_seq))
        iterations = 1000000
        for i in range(iterations):
            try:
                
                registers = execute(parsed_input, iterations, a=i, out=[1])
                # print(f"Testing with a={i}")
                # print(f"Output for a={i}: {registers['out']}")
                if len(registers['out']) >= 10:  # Assuming you want a specific output length
                    print(f"Part 1: a={i}")
                    return
            except BunnyException:
                pass

if __name__ == '__main__':
    main()
