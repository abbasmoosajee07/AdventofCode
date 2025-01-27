
#!/usr/bin/env python3

class Intcode_CPU:
    """
    Simulates an Intcode computer, capable of executing a given Intcode program.

    The Intcode computer interprets and executes an Intcode program, which consists of
    a sequence of instructions represented as integers. The program operates using an
    instruction pointer (pointer) and memory (memory) and follows the rules of the Intcode
    language, supporting operations such as addition, multiplication, input/output, jumps,
    comparisons, and relative base adjustments.

    Attributes:
        program (list[int]): The original Intcode program, stored as a list of integers.
        memory (dict): A dictionary-based memory for dynamic addressable space, initialized
                        with the program values.
        pointer (int): The current position in the program, representing the instruction pointer.
        output_list (list): A list to store the output values generated during program execution.
        paused (bool): A flag indicating if the program is paused (e.g., waiting for input).
        running (bool): A flag indicating if the program is still running or has halted.
        debug (bool): A flag enabling or disabling verbose logging for debugging purposes.
        relative_base (int): The relative base used for addressing in relative mode (opcode 9).
        inputs_queue (list): A queue of inputs that can be used during program execution.
        opcode_map (dict): A mapping of opcodes (integer operation codes) to their corresponding
                            methods that handle the respective operation.

    Methods:
        process_program(external_input=None): Starts and runs the Intcode program, using
                                                external_input to append inputs to the queue.
        get_result(return_type="memory"): Retrieves the result from the program's execution.
                                            The result can be the memory, output, or both.
        replicate(): Create a complete copy of the cpu at that stage.
        __halt(): Halts the program, stopping further execution.
        __arithmetic(operator: str, args_reqd: int): Performs arithmetic operations (addition or multiplication).
        __input(args_reqd: int): Handles the input operation, retrieving input values and storing them in memory.
        __output(args_reqd: int): Handles the output operation, appending output values to the output list.
        __jump_op(jump_if: str, args_reqd: int): Performs conditional jumps based on the value of an argument.
        __comp_op(comparison: str, args_reqd: int): Performs comparison operations (less than or equal).
        __relative(args_reqd: int): Adjusts the relative base used for addressing in relative mode.
        __get_args(total_args: int): Retrieves the required number of arguments from memory starting at the current pointer.
        __get_value(parameter, mode): Fetches a value based on the parameter mode (position, immediate, or relative).
        __write_value(parameter, mode, value): Writes a value to memory, using the specified mode (position or relative).
    """
    def __init__(self, program: list[int], init_inputs=None, pointer: int = 0, debug: bool = False):
        """
        Initialize the Intcode Program.
        """
        # Make a copy of the input program to avoid modifying the original
        self.program = program.copy()

        # Set the initial instruction pointer
        self.pointer = pointer

        # Relative base used for address calculations in mode 2
        self.relative_base = 0

        # Convert the program into a dictionary-based memory for dynamic access
        # Keys represent addresses, and values represent the data at those addresses
        self.memory = {i: v for i, v in enumerate(self.program)}

        # List to store output values generated by the program
        self.output_list = []

        # Flags for execution state
        self.paused = False    # Indicates if the program is paused (e.g., waiting for input)
        self.running = True    # Indicates if the program is still running (not halted)

        # Debugging mode flag
        self.debug = debug     # If True, additional debug information can be printed/logged

        # Initialize the input queue
        if isinstance(init_inputs, list):
            # If inputs are provided as a list, use them directly
            self.inputs_queue = init_inputs
        elif isinstance(init_inputs, int):
            # If a single integer is provided, wrap it in a list
            self.inputs_queue = [init_inputs]
        else:
            # Default to an empty list if no inputs are provided
            self.inputs_queue = []

        self.opcode_map = {
            99: self.__halt,
            1: lambda: self.__arithmetic('add', 4),
            2: lambda: self.__arithmetic('mul', 4),
            3: lambda: self.__input(2),
            4: lambda: self.__output(2),
            5: lambda: self.__jump_op('True',  3),
            6: lambda: self.__jump_op('False', 3),
            7: lambda: self.__comp_op('less',  4),
            8: lambda: self.__comp_op('equal', 4),
            9: lambda: self.__relative(2),
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

    def __arithmetic(self, operator: str, args_reqd: int):
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

    def __jump_op(self, jump_if: str, args_reqd: int):
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

    def __comp_op(self, comparison: str, args_reqd: int):
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
            raise ValueError(f"Invalid return_type '{return_type}'. Must be 'memory', 'output', or 'both'.")

    def replicate(self):
        """
        Create and return a copy of the current Intcode_CPU instance, preserving its state.
        """
        # Create a new instance of Intcode_CPU
        new_cpu = Intcode_CPU(self.program)

        # Copy attributes to the new instance
        new_cpu.memory = self.memory.copy()
        new_cpu.pointer = self.pointer
        new_cpu.relative_base = self.relative_base
        new_cpu.output_list = self.output_list.copy()
        new_cpu.inputs_queue = self.inputs_queue.copy()
        new_cpu.paused = self.paused
        new_cpu.running = self.running
        new_cpu.debug = self.debug

        return new_cpu
