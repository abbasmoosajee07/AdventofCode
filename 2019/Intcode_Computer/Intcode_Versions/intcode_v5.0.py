# Advent of Code - Day 11, Year 2019
# Solution Started: Jan 23, 2025
# Puzzle Link: https://adventofcode.com/2019/day/7
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer v5.0]

#!/usr/bin/env python3

class Intcode_CPU:
    def __init__(self, program: list[int], init_inputs = None, pointer: int = 0, debug: bool = False):
        """
        Initialize the Intcode Program with a copy of the program,
            a pointer, inputs, and optional debugging.
        """
        self.program = program.copy()
        self.pointer = pointer
        self.memory = {i: v for i, v in enumerate(self.program)}  # Dynamic memory
        self.output_list = []  # Stores output values
        self.paused = False    # Paused state
        self.running = True    # Execution flag
        self.debug = debug     # Debugging flag
        self.relative_base = 0 # Relative base for mode 2
        if isinstance(init_inputs, list):
            self.inputs_queue = init_inputs
        elif isinstance(init_inputs, int):
            self.inputs_queue = [init_inputs]
        else:
            self.inputs_queue = []

        self.opcode_map = {
            99: self.__halt,
            1: lambda: self.__arithmetic(operator='add', args_reqd=4),
            2: lambda: self.__arithmetic(operator='mul', args_reqd=4),
            3: lambda: self.__input(args_reqd=2),
            4: lambda: self.__output(args_reqd=2),
            5: lambda: self.__jump_op(jump_if='True',     args_reqd=3),
            6: lambda: self.__jump_op(jump_if='False',    args_reqd=3),
            7: lambda: self.__comp_op(comparison='less',  args_reqd=4),
            8: lambda: self.__comp_op(comparison='equal', args_reqd=4),
            9: lambda: self.__relative(args_reqd=2),
        }


    def __get_args(self, total_args: int):
        """
        Retrieve a list of arguments from memory starting from the current pointer position.
        """
        args_list = []
        for arg_no in range(1, total_args):
            args = self.memory.get(self.pointer + arg_no, 0)
            args_list.append(args)
        return args_list

    def __get_value(self, parameter, mode):
        """
        Fetch the value based on the parameter mode (0: position, 1: immediate, 2: relative).
        """
        if mode == 0:    # Position mode
            return self.memory.get(parameter, 0)
        elif mode == 1:  # Immediate mode
            return parameter
        elif mode == 2:  # Relative mode
            return self.memory.get(self.relative_base + parameter, 0)
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def __write_value(self, parameter, mode, value):
        """Write a value to memory based on the parameter mode."""
        if mode == 0:  # Position mode
            self.memory[parameter] = value
        elif mode == 2:  # Relative mode
            self.memory[self.relative_base + parameter] = value
        else:
            raise ValueError(f"Invalid mode for writing: {mode}")

    def __halt(self):
        """
        Halt the program and stop execution.
        """
        self.running = False
        if self.debug:
            print(f"[{self.pointer:07}: HALT] Program stopped")

    def __arithmetic(self, args_reqd: int, operator: str):
        """
        Perform arithmetic operation based on the operator ('add' or 'mult').
        """
        A_addr, B_addr, target = self.__get_args(args_reqd)
        A_val = self.__get_value(A_addr, self.modes[0])
        B_val = self.__get_value(B_addr, self.modes[1])

        if operator == 'add':
            result = A_val + B_val
        elif operator == 'mul':
            result = A_val * B_val
        else:
            raise ValueError(f"Invalid arithmetic operator: {operator}")

        self.__write_value(target, self.modes[2], result)

        if self.debug:
            print(f"[{self.pointer:07}: {operator.upper()}] A({A_addr}): {A_val}, B({B_addr}): {B_val} -> To({target}): {result}")

        self.pointer += args_reqd

    def __input(self, args_reqd: int):
        """
        Handle input operation: store the input value at the specified location.
        """
        if not self.inputs_queue:
            self.paused = True
            return None # Wait for more input

        target = self.__get_args(args_reqd)[0]
        input_val = self.inputs_queue.pop(0)
        self.__write_value(target, self.modes[0], input_val)

        if self.debug:
            print(f"[{self.pointer:07}: INP] Value({input_val}) -> Addr: {target}")

        self.pointer += args_reqd

    def __output(self, args_reqd: int):
        """
        Handle output operation: append the value at the specified location to the output list.
        """
        source = self.__get_args(args_reqd)[0]
        output_val = self.__get_value(source, self.modes[0])
        self.output_list.append(output_val)

        if self.debug:
            print(f"[{self.pointer:07}: OUT] Value({output_val})")

        self.pointer += args_reqd

        return output_val

    def __jump_op(self, args_reqd: int, jump_if: str):
        """
        Perform jump operations based on the condition (`jump_if`).
        """
        A_addr, B_addr = self.__get_args(args_reqd)
        A_val = self.__get_value(A_addr, self.modes[0])
        B_val = self.__get_value(B_addr, self.modes[1])
        og_pointer = self.pointer

        if (jump_if == 'True' and A_val != 0) or (jump_if == 'False' and A_val == 0):
            self.pointer = B_val
        else:
            self.pointer += args_reqd

        if self.debug:
            condition = "!= 0" if jump_if == 'True' else "== 0"
            print(f"[{og_pointer:07}: JMP] A({A_addr}): {A_val} {condition}, Jumped to: {self.pointer:07}")

    def __comp_op(self, args_reqd: int, comparison: str):
        """
        Perform comparison operations based on the condition (`comparison`).
        """
        A_addr, B_addr, target = self.__get_args(args_reqd)
        A_val = self.__get_value(A_addr, self.modes[0])
        B_val = self.__get_value(B_addr, self.modes[1])

        result = 1 if (comparison == 'less' and A_val < B_val) or (comparison == 'equal' and A_val == B_val) else 0
        self.__write_value(target, self.modes[2], result)

        if self.debug:
            condition = "<" if comparison == 'less' else "=="
            print(f"[{self.pointer:07}: CMP] A({A_addr}): {A_val} {condition} B({B_addr}): {B_val} -> To({target}): {result}")

        self.pointer += args_reqd

    def __relative(self, args_reqd: int):
        source = self.__get_args(args_reqd)[0]
        value = self.__get_value(source, self.modes[0])
        self.relative_base += value

        if self.debug:
            print(f"[{self.pointer:07}: REL] Adjust Relative Base by {value} -> New Base: {self.relative_base}")

        self.pointer += args_reqd

    def process_program(self, external_input=None):
        """
        Start and run the Intcode program. Optionally, provide external input to append to the queue.
        """
        if external_input is not None:
            self.inputs_queue.append(external_input)

        while self.running and not self.paused:
            instruction = self.memory[self.pointer]
            opcode = instruction % 100
            self.modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]  # Parse parameter modes

            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            self.opcode_map[opcode]()  # Execute the corresponding operation

    def get_result(self, return_type: str = "memory"):
        """
        Retrieve the desired result after running the program.
        """
        if return_type == "memory":
            return [self.memory[i] for i in sorted(self.memory.keys())]
        elif return_type == "output":
            return self.output_list
        elif return_type == "both":
            return ([self.memory[i] for i in sorted(self.memory.keys())], self.output_list)
        else:
            raise ValueError(f"Invalid return_type '{return_type}'. Must be 'memory', 'output', 'program', or 'both'.")

# takes no input and produces a copy of itself as output.
test_input_v401 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# should output a 16-digit number.
test_input_v402 = [1102,34915192,34915192,7,4,7,99,0]
# should output the large number in the middle.
test_input_v403 = [104,1125899906842624,99]
cpu_p1 = Intcode_CPU(test_input_v401, debug=False)
cpu_p1.process_program()
output = cpu_p1.get_result('output')
print("test v4.01:", output)

from itertools import permutations
# Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
test_input_v311 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
# Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
test_input_v312 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
def run_amplifiers(program, phase_settings):
    max_signal = 0
    for phases in permutations(phase_settings):
        amplifiers = [Intcode_CPU(program, init_inputs=[phase], debug=False) for phase in phases]
        signal = 0
        while any(a.running for a in amplifiers):  # Run until all amplifiers halt
            for amp in amplifiers:
                if amp.paused:
                    amp.paused = False  # Resume if paused
                amp.process_program(external_input=signal)
                if amp.output_list:  # Check if there's a new output
                    signal = amp.output_list.pop(0)
        max_signal = max(max_signal, signal)
    return max_signal
test_311= run_amplifiers(test_input_v311, range(5, 10))
print(f"Test v3.11: {test_311}")
test_312= run_amplifiers(test_input_v312, range(5, 10))
print(f"Test v3.12: {test_312}")