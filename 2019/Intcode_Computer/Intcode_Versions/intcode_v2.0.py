# Advent of Code - Day 5, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/5
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer v2.0]

class Intcode_CPU:
    def __init__(self, program: list[int], pointer: int = 0, inputs=None, debug: bool = False):
        """
        Initialize the Intcode Program with a copy of the program, a pointer, inputs, and optional debugging.
        """
        self.program = program.copy()
        self.pointer = pointer
        self.inputs_queue = [inputs] if inputs else []
        self.output_list = []  # Stores output values
        self.running = True    # Execution flag
        self.debug = debug     # Debugging flag

        self.opcode_map = {
            1: lambda: self.__arithmetic('add'),
            2: lambda: self.__arithmetic('mult'),
            3: self.__input,
            4: self.__output,
            99: self.__halt,
        }

    def get_value(self, parameter, mode):
        """ Fetch the value based on the parameter mode (0: position, 1: immediate). """
        if mode == 0:  # Position mode
            return self.program[parameter]
        elif mode == 1:  # Immediate mode
            return parameter
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def __arithmetic(self, operator: str):
        """ Perform arithmetic operation based on the operator ('add' or 'mult'). """
        A_addr, B_addr, target = self.program[self.pointer + 1: self.pointer + 4]
        A_val = self.get_value(A_addr, self.modes[0])
        B_val = self.get_value(B_addr, self.modes[1])

        if operator == 'add':
            self.program[target] = A_val + B_val
        elif operator == 'mult':
            self.program[target] = A_val * B_val

        if self.debug:
            print(f"{self.pointer:07}: {operator.upper()} (A {A_addr}:{A_val}) "
                    f"(B {B_addr}:{B_val}) (To {target}:{self.program[target]})")

        self.pointer += 4

    def __input(self):
        """ Handle input operation: store the input value at the specified location. """
        store_to = self.program[self.pointer + 1]
        input_val = self.inputs_queue.pop(0)
        self.program[store_to] = input_val

        if self.debug:
            print(f"{self.pointer:07}: IN  (Store To = {store_to}: Value = {input_val})")

        self.pointer += 2

    def __output(self):
        """ Handle output operation: append the value at the specified location to the output list. """
        store_to = self.program[self.pointer + 1]
        output_val = self.get_value(store_to, self.modes[0])
        self.output_list.append(output_val)

        if self.debug:
            print(f"{self.pointer:07}: OUT (From {store_to}: Value = {output_val})")

        self.pointer += 2

    def __halt(self):
        """ Halt the program and stop execution. """
        self.running = False
        if self.debug:
            print(f"{self.pointer:07}: HALT")
            print(f"Final Program: {self.program}")
            print(f"Output Values: {self.output_list}")

    def process_program(self):
        """ Start and run the Intcode program. """
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

test_input_v21 = [3,0,4,0,99]
test_input_v22 = [1002,4,3,4,33]
test_input_v23 = [1101,100,-1,4,0]

start_cpu = Intcode_CPU(test_input_v22, inputs=1, debug=True)
start_cpu.process_program()
output_p1 = start_cpu.get_result()
diagnostic_code =  next((x for x in output_p1 if x != 0), None)
print("Test v2.0:", output_p1)

