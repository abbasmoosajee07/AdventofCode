# Advent of Code - Day 5, Year 2019
# Solution Started: Jan 21, 2025
# Puzzle Link: https://adventofcode.com/2019/day/5
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer v2.1]

#!/usr/bin/env python3


class Intcode_CPU:
    def __init__(self, program: list[int], pointer: int = 0, inputs=None, debug: bool = False):
        """
        Initialize the Intcode Program with a copy of the program,
            a pointer, inputs, and optional debugging.
        """
        self.program = program.copy()
        self.pointer = pointer
        self.inputs_queue = [inputs] if inputs else []
        self.output_list = []  # Stores output values
        self.running = True    # Execution flag
        self.debug = debug     # Debugging flag

        self.opcode_map = {
            99: self.__halt,
            1: lambda: self.__arithmetic('add'),
            2: lambda: self.__arithmetic('mult'),
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
            print(f"{self.pointer:07}: HALT")
            print(f"Final Program: {self.program}")
            print(f"Output Values: {self.output_list}")

    def __arithmetic(self, operator: str):
        """
        Perform arithmetic operation based on the operator ('add' or 'mult').
        """
        A_addr, B_addr, target = self.program[self.pointer + 1: self.pointer + 4]
        A_val = self.__get_value(A_addr, self.modes[0])
        B_val = self.__get_value(B_addr, self.modes[1])

        if operator == 'add':
            self.program[target] = A_val + B_val
        elif operator == 'mult':
            self.program[target] = A_val * B_val

        if self.debug:
            print(f"{self.pointer:07}: {operator.upper()} (A {A_addr}:{A_val}) "
                    f"(B {B_addr}:{B_val}) (To {target}:{self.program[target]})")

        self.pointer += 4

    def __input(self):
        """
        Handle input operation: store the input value at the specified location.
        """
        store_to = self.program[self.pointer + 1]
        input_val = self.inputs_queue.pop(0)
        self.program[store_to] = input_val

        if self.debug:
            print(f"{self.pointer:07}: IN  (Store To = {store_to}: Value = {input_val})")

        self.pointer += 2

    def __output(self):
        """
        Handle output operation: append the value at the specified location to the output list.
        """
        store_to = self.program[self.pointer + 1]
        output_val = self.__get_value(store_to, self.modes[0])
        self.output_list.append(output_val)

        if self.debug:
            print(f"{self.pointer:07}: OUT (From {store_to}: Value = {output_val})")

        self.pointer += 2

    def __jump_op(self, jump_if: str):
        """
        Perform jump operations based on the condition (`jump_if`).
        """
        A_addr, B_addr = self.program[self.pointer + 1: self.pointer + 3]
        A_val = self.__get_value(A_addr, self.modes[0])
        B_val = self.__get_value(B_addr, self.modes[1])

        if self.debug:
            print(f"{self.pointer:07}: JUMP_{jump_if.upper()} (A {A_addr}:{A_val}) (To {B_addr}:{B_val})")

        if (jump_if == 'True' and A_val != 0) or (jump_if == 'False' and A_val == 0):
            self.pointer = B_val
        else:
            self.pointer += 3

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
            print(f"{self.pointer:07}: COMP_{comparison.upper()} (A {A_addr}:{A_val}) "
                    f"(B {B_addr}:{B_val}) (To {target}:{result})")

        self.pointer += 4

    def process_program(self):
        """
        Start and run the Input program.
        """
        while self.running:
            instruction = self.program[self.pointer]
            opcode = instruction % 100
            self.modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]  # Parse parameter modes

            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            self.opcode_map[opcode]()  # Execute the corresponding operation

    def get_result(self, return_type: str = "program"):
        """ Retrieve the desired result after running the program. """
        if return_type == "program":
            return self.program
        elif return_type == "output":
            return self.output_list
        elif return_type == "both":
            return self.program, self.output_list
        else:
            raise ValueError(f"Invalid return_type '{return_type}'. Must be 'program', 'output', or 'both'.")

test_input_v211 = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
test_input_v212 = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
test_input_v213 = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

start_cpu = Intcode_CPU(test_input_v213, inputs=5, debug=True)
start_cpu.process_program()
output_p1 = start_cpu.get_result('output')
diagnostic_code =  next((x for x in output_p1 if x != 0), None)
print("Test v2.1:", diagnostic_code)

