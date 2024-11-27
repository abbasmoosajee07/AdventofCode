# Advent of Code - Day 24, Year 2021
# Solution Started: Nov 27, 2024
# Puzzle Link: https://adventofcode.com/2021/day/24
# Solution by: [abbasmoosajee07]
# Brief: [ALU Processor]

import os
from typing import List, Tuple

D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)
with open(D24_file_path, 'r', encoding='ascii') as infile:
    input_data = [line.strip() for line in infile.readlines()]

class ArithmeticLogicUnitRegister:
    """
    Descriptor class to handle the reading and writing of the registers in the ALU.
    """

    def __set_name__(self, owner: object, name: str):
        self.name = name

    def __get__(self, obj: object, objtype=None) -> int:
        """Get the value of the register from the internal '_registers' dictionary."""
        return getattr(obj, '_registers')[self.name]

    def __set__(self, obj: object, value: int):
        """Set the value of the register in the internal '_registers' dictionary."""
        getattr(obj, '_registers')[self.name] = value

class ArithmeticLogicUnit:
    """
    A class to simulate the behavior of the Arithmetic Logic Unit (ALU), which performs
    arithmetic and logic operations based on instructions.
    """

    w = ArithmeticLogicUnitRegister()
    x = ArithmeticLogicUnitRegister()
    y = ArithmeticLogicUnitRegister()
    z = ArithmeticLogicUnitRegister()

    def __init__(self, w: int = 0, x: int = 0, y: int = 0, z: int = 0) -> None:
        """Initialize the ALU with values for w, x, y, and z."""
        self._registers = {'w': w, 'x': x, 'y': y, 'z': z}

    def execute(self, instructions: List[str], inputs: List[int] = None) -> None:
        """
        Execute the list of ALU instructions with the provided input values.

        :param instructions: List of ALU instructions to execute.
        :param inputs: List of input values for 'inp' operations.
        """
        inputs = inputs.copy() if inputs else []
        operations = {
            'inp': lambda a, b: int(inputs.pop(0)),
            'add': lambda a, b: self._registers[a] + b,
            'mul': lambda a, b: self._registers[a] * b,
            'div': lambda a, b: int(self._registers[a] / b),
            'mod': lambda a, b: self._registers[a] % b,
            'eql': lambda a, b: int(self._registers[a] == b)
        }

        for instruction in instructions:
            operation, arg_a, arg_b = (instruction + ' 0').split(' ')[:3]
            arg_b = self._registers[arg_b] if arg_b.isalpha() else int(arg_b)
            self._registers[arg_a] = operations[operation](arg_a, arg_b)

def get_value(alu_dict, value):
    """Get the value from the ALU dictionary or return the number itself."""
    if isinstance(value, int):  # If it's a number, return it directly
        return value
    elif value in alu_dict:  # If it's a variable, return its value from the dictionary
        return alu_dict[value]
    else:
        raise ValueError(f"Unknown variable: {value}")

def check_version_number(instructions: List[str], version_number: int) -> bool:
    """
    Check if a given version number results in z = 0 when processed by the ALU.

    :param instructions: The ALU instructions to execute.
    :param version_number: The 14-digit version number to check.
    :return: True if z is 0 after executing the instructions with this version number, else False.
    """
    alu = ArithmeticLogicUnit()
    alu.execute(instructions, [int(d) for d in str(version_number)])
    return alu.z == 0

def find_digits(left: int, right: int, find_max: bool = True) -> Tuple[int, int]:
    """
    Find the values for two digits based on the given 'left' and 'right' values.
    
    :param left: The left operand from the ALU instructions.
    :param right: The right operand from the ALU instructions.
    :param find_max: Whether to find the maximum or minimum values for the digits.
    :return: A tuple of the two digits.
    """
    if find_max:
        if left + right <= 0:
            return 9, 9 + left + right
        else:
            return 9 - left - right, 9
    else:
        if left + right <= 0:
            return 1 - left - right, 1
        else:
            return 1, 1 + left + right

def calculate_version(instructions: List[str], find_max: bool = True) -> int:
    """
    Calculate the 14-digit version number based on the ALU instructions.

    :param instructions: List of ALU instructions.
    :param find_max: If True, find the largest version number. If False, find the smallest.
    :return: The calculated version number.
    """
    instruction_sets = []
    for instruction in instructions:
        if instruction.startswith('inp'):
            instruction_sets.append([])  # Start a new set when encountering 'inp'
        instruction_sets[-1].append(instruction)

    version_number_digits: List[int] = [None] * len(instruction_sets)
    left_digit_stack = []  # Stack to keep track of the left-side instructions

    for i in range(len(instruction_sets)):
        if instruction_sets[i][4] == 'div z 1':
            left_digit_stack.append((i, instruction_sets[i]))
        else:
            left_i, left_instruction_set = left_digit_stack.pop()
            left_increment = int(left_instruction_set[15].split(' ')[2])
            right_increment = int(instruction_sets[i][5].split(' ')[2])
            version_number_digits[left_i], version_number_digits[i] = \
                find_digits(left_increment, right_increment, find_max)

    return int(''.join(map(str, version_number_digits)))

# Solve Part 1
ans_p1 = calculate_version(input_data, find_max=True)
print(f'Part 1: {ans_p1}')

# Solve Part 2
ans_p2 = calculate_version(input_data, find_max=False)
print(f'Part 2: {ans_p2}')
