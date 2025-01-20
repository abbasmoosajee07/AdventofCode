import copy

class Intcode_Program:
    def __init__(self, program: list[int], pointer: int = 0, debug: bool = False):
        """
        Initialize the Intcode Program with a copy of the program, a pointer, and optional debugging.
        """
        self.program = copy.deepcopy(program)
        self.pointer = pointer
        self.running = True  # Flag to manage the loop
        self.debug = debug  # Debug flag
        self.opcode_map = {
            1: lambda: self.__arithmetic('add'),
            2: lambda: self.__arithmetic('mult'),
            99: self.__halt,
        }

    def __arithmetic(self, operator: str):
        """
        Perform arithmetic operation based on the operator ('add' or 'mult').
        """
        pointer = self.pointer
        A_addr, B_addr, target = self.program[pointer + 1: pointer + 4]

        if self.debug:
            op_str = f"(A{A_addr}:{self.program[A_addr]}) (B{B_addr}:{self.program[B_addr]}) (to{target}:{self.program[target]})"
            print(f"{pointer:07}: {operator.upper()} {op_str}")

        if operator == 'add':
            self.program[target] = self.program[A_addr] + self.program[B_addr]
        elif operator == 'mult':
            self.program[target] = self.program[A_addr] * self.program[B_addr]

        self.pointer += 4  # Move to the next instruction

    def __halt(self):
        """
        Halt the program and stop execution.
        """
        self.running = False
        if self.debug:
            print(f"{self.pointer:07}: HALT")

    def process_program(self):
        """
        Start and run the Intcode program.
        """
        while self.running:
            opcode = self.program[self.pointer]
            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            # Execute the operation based on the opcode
            self.opcode_map[opcode]()  # Executes the correct lambda function or method

        return self.program

