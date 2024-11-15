# Advent of Code - Day 16, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/16
# Solution by: [abbasmoosajee07]
# Brief: [Identifying register functions, P1]

#!/usr/bin/env python3
import os

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

class OpcodeComputer:
    def __init__(self, registers, A, B, C):
        self.registers = registers
        self.A = A
        self.B = B
        self.C = C

    # Add Registers
    def addr(self): return self._apply_op(self.registers[self.A] + self.registers[self.B])
    def addi(self): return self._apply_op(self.registers[self.A] + self.B)

    # Multiply Registers
    def mulr(self): return self._apply_op(self.registers[self.A] * self.registers[self.B])
    def muli(self): return self._apply_op(self.registers[self.A] * self.B)

    # Bitwise AND
    def banr(self): return self._apply_op(self.registers[self.A] & self.registers[self.B])
    def bani(self): return self._apply_op(self.registers[self.A] & self.B)

    # Bitwise OR
    def borr(self): return self._apply_op(self.registers[self.A] | self.registers[self.B])
    def bori(self): return self._apply_op(self.registers[self.A] | self.B)

    # Assignment operations
    def setr(self): return self._apply_op(self.registers[self.A])
    def seti(self): return self._apply_op(self.A)

    # Greater-than testing
    def gtir(self): return self._apply_op(1 if self.A > self.registers[self.B] else 0)
    def gtri(self): return self._apply_op(1 if self.registers[self.A] > self.B else 0)
    def gtrr(self): return self._apply_op(1 if self.registers[self.A] > self.registers[self.B] else 0)

    # Equality testing
    def eqir(self): return self._apply_op(1 if self.A == self.registers[self.B] else 0)
    def eqri(self): return self._apply_op(1 if self.registers[self.A] == self.B else 0)
    def eqrr(self): return self._apply_op(1 if self.registers[self.A] == self.registers[self.B] else 0)

    def _apply_op(self, value):
        result = self.registers.copy()
        result[self.C] = value
        return result


# Operations map for easier access
OPERATIONS = {
    'addr': OpcodeComputer.addr,
    'addi': OpcodeComputer.addi,
    'mulr': OpcodeComputer.mulr,
    'muli': OpcodeComputer.muli,
    'banr': OpcodeComputer.banr,
    'bani': OpcodeComputer.bani,
    'borr': OpcodeComputer.borr,
    'bori': OpcodeComputer.bori,
    'setr': OpcodeComputer.setr,
    'seti': OpcodeComputer.seti,
    'gtir': OpcodeComputer.gtir,
    'gtri': OpcodeComputer.gtri,
    'gtrr': OpcodeComputer.gtrr,
    'eqir': OpcodeComputer.eqir,
    'eqri': OpcodeComputer.eqri,
    'eqrr': OpcodeComputer.eqrr,
}


def parse_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    samples, instructions = [], []
    i = 0

    # Parse samples (before/after cases for mapping)
    while lines[i].startswith("Before"):
        before = eval(lines[i][8:])
        instruction = list(map(int, lines[i+1].split()))
        after = eval(lines[i+2][8:])
        samples.append((before, instruction, after))
        i += 4  # Skip "Before", instruction, "After", and blank line

    # Remaining lines are the program instructions for part 2
    instructions = [list(map(int, line.split())) for line in lines[i+1:] if line.strip()]
    return samples, instructions


def possible_operations(before, instruction, after):
    """Determine which operations match the given instruction and states."""
    opcode, A, B, C = instruction
    matches = set()
    
    for op_name, op_func in OPERATIONS.items():
        computer = OpcodeComputer(before, A, B, C)
        # Directly call the operation method and compare the result
        if op_func(computer) == after:
            matches.add(op_name)
    
    return matches


def deduce_opcode_mapping(samples):
    """Deduce the mapping of opcodes to operations."""
    opcode_mapping = {opcode: set(OPERATIONS.keys()) for opcode in range(16)}
    
    # Reduce possibilities by intersecting with possible operations
    for before, instruction, after in samples:
        opcode = instruction[0]
        opcode_mapping[opcode].intersection_update(possible_operations(before, instruction, after))
    
    # Resolve each opcode to a single operation
    resolved = {}
    while len(resolved) < len(opcode_mapping):
        for opcode, ops in opcode_mapping.items():
            if len(ops) == 1:
                op_name = ops.pop()
                resolved[opcode] = op_name
                # Remove this resolved operation from other opcode sets
                for other_ops in opcode_mapping.values():
                    other_ops.discard(op_name)
    
    return resolved


def execute_instructions(instructions, opcode_map):
    """Execute the list of instructions with resolved opcodes."""
    registers = [0, 0, 0, 0]
    
    for instruction in instructions:
        opcode, A, B, C = instruction
        operation_name = opcode_map[opcode]
        computer = OpcodeComputer(registers, A, B, C)
        registers = getattr(computer, operation_name)()
    
    return registers[0]


def count_samples_with_multiple_matches(samples):
    """Count samples that match 3 or more possible operations."""
    count = 0
    for before, instruction, after in samples:
        if len(possible_operations(before, instruction, after)) >= 3:
            count += 1
    return count


samples, instructions = parse_input_file(D16_file_path)

# Part 1
part1_result = count_samples_with_multiple_matches(samples)
print("Part 1:", part1_result)
# First Guess: 4181 too high
# Second Guess: 3572 too high
# Correct: 640 not opcode count, simple check count

# Part 2
opcode_map = deduce_opcode_mapping(samples)
part2_result = execute_instructions(instructions, opcode_map)
print("Part 2:", part2_result)




