# Advent of Code - Day 23, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/23
# Solution by: [abbasmoosajee07]
# Brief: [Register Computing V2]

import os
import pandas as pd

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

with open(D23_file_path) as file:
    input_data = file.read().strip().split('\n')

# Parse the input data into a DataFrame
def parse_instructions(input_data):
    commands = []
    for line in input_data:
        parts = line.split()
        # Ensure we handle missing 'Y' by filling it with None
        command = parts[0]
        X = parts[1] if len(parts) > 1 else None
        Y = parts[2] if len(parts) > 2 else None
        commands.append((command, X, Y))
    return pd.DataFrame(commands, columns=['command', 'X', 'Y'])

class SoundProcessor:
    def __init__(self):
        self.registers = {} 
        self.last_sound = None
        self.pointer = 0

    def get_value(self, operand):
        """Return the integer value of operand or register content if it's a register."""
        if operand is None:
            return 0
        if operand.lstrip('-').isdigit() or operand.lstrip('+').isdigit():
            return int(operand)
        return self.registers.get(operand, 0)

    def snd(self, X):
        """Play sound with the frequency given by the value of X."""
        self.last_sound = self.get_value(X)

    def set_reg(self, X, Y):
        """Set register X to the value of Y."""
        self.registers[X] = self.get_value(Y)

    def add(self, X, Y):
        """Increase register X by the value of Y."""
        self.registers[X] = self.registers.get(X, 0) + self.get_value(Y)

    def sub(self, X, Y):
        """Decrease register X by the value of Y."""
        self.registers[X] = self.registers.get(X, 0) - self.get_value(Y)

    def mul(self, X, Y):
        """Set register X to the result of multiplying register X by Y."""
        self.registers[X] = self.registers.get(X, 0) * self.get_value(Y)

    def mod(self, X, Y):
        """Set register X to the remainder of dividing register X by Y."""
        if self.get_value(Y) != 0:
            self.registers[X] = self.registers.get(X, 0) % self.get_value(Y)

    def rcv(self, X):
        """Recover the frequency of the last sound if X is non-zero."""
        if self.get_value(X) != 0:
            print(f"Recovered frequency: {self.last_sound}")
            return self.last_sound
        return None

    def jnz(self, X, Y):
        """Jump with an offset of Y if X is greater than zero."""
        if self.get_value(X) != 0:
            return self.get_value(Y)
        return 1

    def execute_command(self, command, X, Y, mul_count):
        """Execute the specified command with given operands."""
        if command == 'snd':
            self.snd(X)
        elif command == 'set':
            self.set_reg(X, Y)
        elif command == 'add':
            self.add(X, Y)
        elif command == 'sub':
            self.sub(X, Y)
        elif command == 'mul':
            mul_count += 1
            # print(mul_count)
            self.mul(X, Y)
        elif command == 'mod':
            self.mod(X, Y)
        elif command == 'rcv':
            result = self.rcv(X)
            if result is not None:
                return result, mul_count
        elif command == 'jnz':
            offset = self.jnz(X, Y)
            self.pointer += offset - 1  # Adjust pointer by offset-1 to account for pointer increment in `run`
        return None, mul_count

    def run(self, df):
        """Execute instructions until an `rcv` command recovers a frequency or instructions end."""
        mul_count = 0
        while 0 <= self.pointer < len(df):
            command, X, Y = df.loc[self.pointer]
            result, mul_count = self.execute_command(command, X, Y, mul_count)
            if result is not None:
                return result, mul_count
            self.pointer += 1
        return df, mul_count

# Example usage
df = parse_instructions(input_data)
processor = SoundProcessor()
final_df, mul_count = processor.run(df)
print(f"Part 1: The 'mul' operation was called {mul_count} times.")

# Part 2: Direct computation based on observed patterns in the instruction set
def count_non_primes_in_range(start, end, step):
    """Count numbers in the specified range that are NOT prime."""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    count_non_primes = sum(1 for n in range(start, end + 1, step) if not is_prime(n))
    return count_non_primes

# Parameters derived from analysis of Part 2 instructions
# Starting values for analysis
initial_b = df[df['X']=='b']
initial_b = int(initial_b[initial_b['command'] == 'set']['Y'].loc[0])
start = initial_b * 100 + 100000  # 106500
end = start + 17000  # 123500
step = 17


non_prime_count = count_non_primes_in_range(start, end, step)
print(f"Part 2: The count of non-prime numbers in the range is {non_prime_count}.")
