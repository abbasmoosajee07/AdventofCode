import copy

class Intcode_Program:
    def __init__(self, program: list[int], pointer: int = 0):
        self.program = copy.deepcopy(program)
        self.pointer = pointer
        self.running = True  # Flag to manage the loop
        self.opcode_map = {
            1: lambda: self.__arithmetic('add'),
            2: lambda: self.__arithmetic('mult'),
            99: self.__halt,
        }

    def __arithmetic(self, operator: str):
        pointer = self.pointer
        # Dereference values based on program's addressing
        A_addr, B_addr, target= self.program[pointer + 1: pointer + 4]
        if operator == 'add':
            self.program[target] = self.program[A_addr] + self.program[B_addr]
        elif operator == 'mult':
            self.program[target] = self.program[A_addr] * self.program[B_addr]
        self.pointer += 4  # Move to the next instruction

    def __halt(self):
        self.running = False  # Stop the program
        # print("Program halted.")
        # print("Final state:", self.program)

    def process_program(self):
        while self.running:
            opcode = self.program[self.pointer]
            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")
            self.opcode_map[opcode]()  # Execute the mapped function

        return self.program
