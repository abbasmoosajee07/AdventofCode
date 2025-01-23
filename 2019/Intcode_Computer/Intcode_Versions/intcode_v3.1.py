# Advent of Code - Day 7, Year 2019
# Solution Started: Jan 23, 2025
# Puzzle Link: https://adventofcode.com/2019/day/7
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer v3.1]

#!/usr/bin/env python3

from itertools import permutations

class Intcode_CPU:
    def __init__(self, program: list[int], pointer: int = 0, inputs=None, debug: bool = False):
        """
        Initialize the Intcode Program with a copy of the program,
            a pointer, inputs, and optional debugging.
        """
        self.program = program.copy()
        self.pointer = pointer
        self.output_list = []  # Stores output values
        self.paused = False    # Paused state
        self.running = True    # Execution flag
        self.debug = debug     # Debugging flag
        if isinstance(inputs, list):
            self.inputs_queue = inputs
        elif isinstance(inputs, int):
            self.inputs_queue = [inputs]
        elif inputs:
            self.inputs_queue = []

        self.opcode_map = {
            99: self.__halt,
            1: lambda: self.__arithmetic('add'),
            2: lambda: self.__arithmetic('mul'),
            3: self.__input,
            4: self.__output,
            5: lambda: self.__jump_op('True'),
            6: lambda: self.__jump_op('False'),
            7: lambda: self.__comp_op('less'),
            8: lambda: self.__comp_op('equal'),
        }

    def __get_value(self, parameter, mode):
        """
        Fetch the value based on the parameter mode (0: position, 1: immediate).
        """
        if mode == 0:  # Position mode
            return self.program[parameter]
        elif mode == 1:  # Immediate mode
            return parameter
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def __halt(self):
        """
        Halt the program and stop execution.
        """
        self.running = False
        if self.debug:
            print(f"[{self.pointer:07}: HALT] Program stopped")

    def __arithmetic(self, operator: str):
        """
        Perform arithmetic operation based on the operator ('add' or 'mult').
        """
        A_addr, B_addr, target = self.program[self.pointer + 1: self.pointer + 4]
        A_val = self.__get_value(A_addr, self.modes[0])
        B_val = self.__get_value(B_addr, self.modes[1])

        if operator == 'add':
            self.program[target] = A_val + B_val
        elif operator == 'mul':
            self.program[target] = A_val * B_val

        if self.debug:
            print(f"[{self.pointer:07}: {operator.upper()}] A({A_addr}): {A_val}, B({B_addr}): {B_val} -> To({target}): {self.program[target]}")

        self.pointer += 4

    def __input(self):
        """
        Handle input operation: store the input value at the specified location.
        """
        if not self.inputs_queue:
            self.paused = True
            return  # Wait for more input
        store_to = self.program[self.pointer + 1]
        input_val = self.inputs_queue.pop(0)
        self.program[store_to] = input_val

        if self.debug:
            print(f"[{self.pointer:07}: INP] Value({store_to}): {input_val} -> Addr: {store_to}")

        self.pointer += 2

    def __output(self):
        """
        Handle output operation: append the value at the specified location to the output list.
        """
        store_to = self.program[self.pointer + 1]
        output_val = self.__get_value(store_to, self.modes[0])
        self.output_list.append(output_val)

        if self.debug:
            print(f"[{self.pointer:07}: OUT] Value({store_to}): {output_val}")

        self.pointer += 2

        return output_val

    def __jump_op(self, jump_if: str):
        """
        Perform jump operations based on the condition (`jump_if`).
        """
        A_addr, B_addr = self.program[self.pointer + 1: self.pointer + 3]
        A_val = self.__get_value(A_addr, self.modes[0])
        B_val = self.__get_value(B_addr, self.modes[1])


        if (jump_if == 'True' and A_val != 0) or (jump_if == 'False' and A_val == 0):
            self.pointer = B_val
            pointer_jump = B_val
        else:
            self.pointer += 3
            pointer_jump = 3

        if self.debug:
            condition = "!= 0" if jump_if == 'True' else "== 0"
            print(f"[{self.pointer:07}: JMP] A({A_addr}): {A_val} {condition}, Jump By: {pointer_jump}")

    def __comp_op(self, comparison: str):
        """
        Perform comparison operations based on the condition (`comparison`).
        """
        A_addr, B_addr, target = self.program[self.pointer + 1: self.pointer + 4]
        A_val = self.__get_value(A_addr, self.modes[0])
        B_val = self.__get_value(B_addr, self.modes[1])

        result = 1 if (comparison == 'less' and A_val < B_val) or (comparison == 'equal' and A_val == B_val) else 0
        self.program[target] = result

        if self.debug:
            condition = "<" if comparison == 'less' else "=="
            print(f"[{self.pointer:07}: CMP] A({A_addr}): {A_val} {condition} B({B_addr}): {B_val} -> To({target}): {result}")

        self.pointer += 4

    def process_program(self):
        """
        Start and run the Intcode program.
        """
        while self.running and not self.paused:
            instruction = self.program[self.pointer]
            opcode = instruction % 100
            self.modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]  # Parse parameter modes

            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            self.opcode_map[opcode]()  # Execute the corresponding operation

    def get_result(self, return_type: str = "program"):
        """
        Retrieve the desired result after running the program.
        """
        if return_type == "program":
            return self.program
        elif return_type == "output":
            return self.output_list
        elif return_type == "both":
            return self.program, self.output_list
        else:
            raise ValueError(f"Invalid return_type '{return_type}'. Must be 'program', 'output', or 'both'.")


# Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
test_input_v311 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

# Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
test_input_v312 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

def run_amplifiers(program, phase_settings):
    max_signal = 0
    for phases in permutations(phase_settings):
        amplifiers = [Intcode_CPU(program, inputs=[phase], debug=False) for phase in phases]
        signal = 0

        while any(a.running for a in amplifiers):  # Run until all amplifiers halt
            for amp in amplifiers:
                if amp.paused:
                    amp.paused = False  # Resume if paused
                amp.inputs_queue.append(signal)
                amp.process_program()
                if amp.output_list:  # Check if there's a new output
                    signal = amp.output_list.pop(0)
        
        max_signal = max(max_signal, signal)
    
    return max_signal

test_311= run_amplifiers(test_input_v311, range(5, 10))
print(f"Test v3.11: {test_311}")

test_312= run_amplifiers(test_input_v312, range(5, 10))
print(f"Test v3.12: {test_312}")