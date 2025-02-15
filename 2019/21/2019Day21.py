"""Advent of Code - Day 21, Year 2019
Solution Started: Feb 11, 2025
Puzzle Link: https://adventofcode.com/2019/day/21
Solution by: abbasmoosajee07
Brief: [Intcode Springdroid]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
start_time = time.time()

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)
# from Intcode_Computer import Intcode_CPU
# from z3 import BoolVal, BitVec, Bool, If, And, Not, Or, substitute, Solver, sat

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Springdroid:
    """
    A specialized Intcode computer designed to execute SpringScript programs 
    for controlling a droid in a terrain traversal problem.

    This class integrates an Intcode-based virtual machine with SpringScript logic, 
    allowing the droid to analyze terrain, generate movement scripts, and execute them 
    to determine safe traversal paths.
    """
    MAX_MEMORY = 15

    def __init__(self, droid_cpu: list[int]):
        from Intcode_Computer import Intcode_CPU
        self.droid_code = droid_cpu
        self.droid = Intcode_CPU(droid_cpu, debug=False)

    def run_droids(self, script: str, visualize: bool = False):
        """
        Executes a given SpringScript program using a droid, optionally visualizing the terrain.

        This method takes a SpringScript program as input, replicates the droid, and feeds
        each instruction as external input to the droid. It can visualize the output if required.
        """
        inp_list = [ord(val) for val in list(script)]
        use_droid = self.droid.replicate()

        for num in inp_list:
            use_droid.paused = False
            use_droid.process_program(external_input=num)
        if visualize:
            self.print_hull(use_droid.get_result('output')[:-1], True)
        output = use_droid.get_result('output')
        return output

    @staticmethod
    def print_hull(droid_output: list[int], visualize: bool = True) -> list[str]:
        """
        Display the hull in the current state.
        """
        hull_grid = ''.join(map(chr, droid_output))
        hull_rows = hull_grid.strip().split('\n')

        if visualize:
            print('\n'.join(hull_rows))
            print("_" * len(hull_rows[0]))

        return hull_rows

    @staticmethod
    def symbolic_execution(step_registers: str, length: int = MAX_MEMORY):
        """
        Symbolically executes a program of a given length

        Returns (f, prog):
        - f is a lambda function which should be called with a map
            of sensor readings, and returns the symbolic result
        - prog is a list of (opcode, reg_in, reg_out) tuples
        """
        from z3 import BoolVal, BitVec, Bool, If, And, Not, Or, substitute
        # Initialize the T and J registers to False
        T = BoolVal(False)
        J = BoolVal(False)
        sensors = {c: Bool(c) for c in step_registers}
        program = []

        for i in range(length):
            op = BitVec('op_%i' % i, 2)
            reg_in = BitVec('reg_in_%i' % i, 4)
            reg_out = BitVec('reg_out_%i' % i, 1)

            lhs = T  # default value
            for (i, r) in enumerate(list(sensors.values()) + [T, J]):
                lhs = If(reg_in == i, r, lhs)

            rhs = If(reg_out == 0, T, J)
            result = If(op == 0, And(lhs, rhs),
                        If(op == 1, Or(lhs, rhs),
                                    Not(lhs)))

            (T, J) = (If(reg_out == 0, result, T),
                        If(reg_out == 1, result, J))

            program.append([op, reg_in, reg_out])

        f = lambda vs: substitute(J,
            *[(v, BoolVal(vs[k]) if type(vs[k]) is bool else vs[k])
                for (k, v) in sensors.items()])

        return (f, program)

    @staticmethod
    def decode(prog, model, step_registers: str):
        """
        Converts a program + solved model into SpringScript
        """
        if len(model) == 0:
            return ' '
        ops = {0: 'AND', 1: 'OR', 2: 'NOT'}
        input_registers = step_registers + "TJ"
        inputs = {i: c for (i, c) in enumerate(input_registers)}
        outputs = {0: 'T', 1: 'J'}
        script = ''
        for (op, reg_in, reg_out) in prog:
            op = model.eval(op).as_long()
            reg_in = model.eval(reg_in).as_long()
            reg_out = model.eval(reg_out).as_long()

            op = ops.get(op, 'NOT')
            reg_in = inputs.get(reg_in, 'T')
            reg_out = outputs.get(reg_out, 'T')
            script += "%s %s %s\n" % (op, reg_in, reg_out)
        return script[:-1]

    def solve_for_maps(self, maps, step_registers: str, length: int = MAX_MEMORY):
        """
        Uses symbolic execution and constraint solving to determine a valid
        SpringScript program that ensures safe traversal of given terrain maps.
        """
        from z3 import Solver, And, Not, Or, sat
        (j, prog) = self.symbolic_execution(step_registers, length)
        solver = Solver()
        for m in maps:
            jumps_at = []
            for (i, c) in enumerate(m):
                airborn = Or(jumps_at[-3:])
                if c != '#':
                    solver.add(airborn)
                sensors = {c: i + j + 1 >= len(m) or m[i + j + 1] == '#'
                            for (j, c) in enumerate(step_registers)}
                jumps_at.append(And(Not(airborn), j(sensors)))
        r = solver.check()
        return self.decode(prog, solver.model(), step_registers) if r == sat else False

    def minimize_for_maps(self, maps: list[str], step_registers: str) -> str:
        """
        Finds the smallest program length that successfully solves all given terrain maps.

        This function iteratively increases the allowed program length, starting from 5,
        and attempts to solve the maps using `solve_for_maps`. It returns the first valid
        SpringScript program found.
        """
        for i in range(5, self.MAX_MEMORY + 1):
            # Call the multi-map function instead
            r = self.solve_for_maps(maps, step_registers, i)
            if r:
                return r
        return False

    def analyze_terrain(self, droid_script: str, outputs: list[int] = None) -> str:
        """
        Analyzes the terrain directly below the droid based on either provided outputs
        or by executing the given SpringScript program.
        """
        if outputs:
            test_output = outputs
        else:
            test_output = self.run_droids(droid_script, visualize=False)
        hull_map = self.print_hull(test_output, visualize=False)

        for row_no, row in enumerate(hull_map):
            if len(row) >= 1 and row[0] == "@":
                droid_pos = row_no
                break
        terrain = hull_map[droid_pos + 1]
        return terrain

    def write_springscript(self, speed: str, test_script: str = None, full_map: list[str] = [],
                            outputs: list[int] = [], visualize: bool = False):
        """
        Iteratively generates a valid SpringScript program that allows the droid
        to traverse the given terrain, ensuring it has at most 15 instructions.
        """
        if test_script is None:
            test_script = speed + "\n"
            instructions = []
        else:
            instructions = test_script.split('\n')[:-2]

        step_registers = "ABCD" if speed == "WALK" else "ABCDEFGHI"
        terrain = self.analyze_terrain(test_script, outputs)
        new_command = self.solve_for_maps([terrain], step_registers)

        instructions.append(new_command)
        full_map.append(terrain)
        droid_script = "\n".join(instructions) + f"{speed}\n"

        if len(droid_script) >= 7 * self.MAX_MEMORY:
            droid_script = self.minimize_for_maps(full_map, step_registers)
            droid_script += f"\n{speed}\n"

        current_output = self.run_droids(droid_script, visualize)
        if max(current_output) >= 128:
            if visualize:
                print("Final Droid Map\n", "\n".join(full_map), sep="")
                print("Final Droid Script\n", droid_script, sep="")
                print("Hull Damage:", max(current_output))
            return droid_script, current_output

        return self.write_springscript(speed, droid_script, full_map, current_output, visualize)

method = " "
springdroids = Intcode_Springdroid(input_program)

if method == "z3":
    walk_script, walk_score = springdroids.write_springscript("WALK", visualize=False)
    run_script, run_score = springdroids.write_springscript("RUN", visualize=False)

else:
    walk_script = """\
        NOT A J
        NOT B T
        OR T J
        NOT C T
        OR T J
        AND D J
        WALK
        """

    run_script ="""\
        NOT A J
        NOT B T
        OR T J
        NOT C T
        OR T J
        AND D J
        NOT H T
        NOT T T
        OR E T
        AND T J
        RUN
        """
    walk_score = springdroids.run_droids(walk_script)
    run_score  = springdroids.run_droids(run_script)

print("Part 1:", max(walk_score))
print("Part 2:", max(run_score))

print(f"Execution Time = {time.time() - start_time:.5f}s")
