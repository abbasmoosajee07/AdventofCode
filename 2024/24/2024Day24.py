"""Advent of Code - Day 24, Year 2024
Solution Started: Dec 24, 2024
Puzzle Link: https://adventofcode.com/2024/day/24
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
"""

#!/usr/bin/env python3

import os, re, copy, time, graphlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()
# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_input(input_list: list[str]) -> tuple[dict, list]:
    wires = {}
    for wire in input_list[0].split('\n'):
        name, value = wire.split(': ')
        wires[name] = int(value)
    gates = []
    for no, line in enumerate(input_list[1].split('\n')):
        inp, out = line.split(' -> ')
        inp1, op, inp2 = inp.split(' ')
        gates.append({'inp1':inp1, 'op':op, 'inp2':inp2, 'out':out})
    return wires, gates

def simulate_circuit(wires_init: dict, gates_list: list) -> dict:
    """
    Simulates a logic circuit based on initial wire states and a list of gates.

    Args:
        wires_init (dict): Dictionary of initial wire states, e.g., {'A': 1, 'B': 0}.
        gates_list (list): List of logic gates. Each gate is a dictionary with keys:
            - 'inp1': Name of the first input wire.
            - 'inp2': Name of the second input wire.
            - 'op': The operation ('AND', 'OR', 'XOR').
            - 'out': The name of the output wire.

    Returns:
        dict: Final wire states after simulating the circuit.
    """
    all_wires = copy.deepcopy(wires_init)
    pending_gates = gates_list.copy()  # Copy gates to avoid modifying the original list

    while pending_gates:
        progress_made = False  # Track progress in each iteration

        for i in range(len(pending_gates) - 1, -1, -1):  # Process gates in reverse order
            test_gate = pending_gates[i]
            input_1 = test_gate['inp1']
            input_2 = test_gate['inp2']
            out_wire = test_gate['out']

            # Check if inputs are available
            if input_1 in all_wires and input_2 in all_wires:
                oper = test_gate['op']

                # Perform the logical operation
                if oper == 'OR':
                    result = int(all_wires[input_1] == 1 or all_wires[input_2] == 1)
                elif oper == 'AND':
                    result = int(all_wires[input_1] == 1 and all_wires[input_2] == 1)
                elif oper == 'XOR':
                    result = int(all_wires[input_1] != all_wires[input_2])
                else:
                    raise ValueError(f"Unknown operation: {oper}")

                # Update the output wire and remove the processed gate
                all_wires[out_wire] = result
                pending_gates.pop(i)
                progress_made = True

        # If no progress was made, raise an error for unresolved gates
        if not progress_made:
            raise ValueError("Circuit simulation stuck: Missing or circular dependencies among gates.")

    return all_wires

def find_wire_group(final_wires: dict, group: str = 'z'):
    # Filter and sort wires starting with group letter
    selected_wires = {k: v for k, v in final_wires.items() if k.startswith(group)}
    sorted_sel_wires = sorted(selected_wires.items())  # Sort by keys (wire names)
    sorted_bits = ''.join(str(value) for _, value in sorted_sel_wires[::-1])  # Combine sorted values into a binary string

    # Convert binary to decimal
    decimal_output = int(sorted_bits, 2)

    return decimal_output

test_input_1 = ['x00: 0\nx01: 1\nx02: 0\nx03: 1\nx04: 0\nx05: 1\ny00: 0\ny01: 0\ny02: 1\ny03: 1\ny04: 0\ny05: 1', 'x00 AND y00 -> z00\nx01 AND y01 -> z01\nx02 AND y02 -> z02\nx03 AND y03 -> z03\nx04 AND y04 -> z04\nx05 AND y05 -> z05']
test_input_2 = ['x00: 1\nx01: 0\nx02: 1\nx03: 1\nx04: 0\ny00: 1\ny01: 1\ny02: 1\ny03: 1\ny04: 1', 'ntg XOR fgs -> mjb\ny02 OR x01 -> tnw\nkwq OR kpj -> z05\nx00 OR x03 -> fst\ntgd XOR rvg -> z01\nvdt OR tnw -> bfw\nbfw AND frj -> z10\nffh OR nrd -> bqk\ny00 AND y03 -> djm\ny03 OR y00 -> psh\nbqk OR frj -> z08\ntnw OR fst -> frj\ngnj AND tgd -> z11\nbfw XOR mjb -> z00\nx03 OR x00 -> vdt\ngnj AND wpb -> z02\nx04 AND y00 -> kjc\ndjm OR pbm -> qhw\nnrd AND vdt -> hwm\nkjc AND fst -> rvg\ny04 OR y02 -> fgs\ny01 AND x02 -> pbm\nntg OR kjc -> kwq\npsh XOR fgs -> tgd\nqhw XOR tgd -> z09\npbm OR djm -> kpj\nx03 XOR y03 -> ffh\nx00 XOR y04 -> ntg\nbfw OR bqk -> z06\nnrd XOR fgs -> wpb\nfrj XOR qhw -> z04\nbqk OR frj -> z07\ny03 OR x01 -> nrd\nhwm AND bqk -> z03\ntgd XOR rvg -> z12\ntnw OR pbm -> gnj']

init_wires, gates = parse_input(input_data)
wires_p1 = simulate_circuit(init_wires, gates)
dec_num_p1 = find_wire_group(wires_p1)
print("Part 1:", dec_num_p1)

# Initialize gate dictionary
g = {gate['out']: (gate['op'], gate['inp1'], gate['inp2']) for gate in gates}

# Find maximum index for wire names
c = max(int(wire[1:]) for wire in g if re.fullmatch(r"z[0-9]+", wire))
m = 2 ** (c + 1) - 1

# Cache the results of test1 and testn to avoid recomputation
test1_cache = {}
testn_cache = {}

# Test function for gate evaluation with memoization
def test1(e, x, y, s):
    # Use a tuple to hash the state and avoid recomputation
    cache_key = tuple(e), x, y, tuple(s.items())
    if cache_key in test1_cache:
        return test1_cache[cache_key]
    
    v = (
        {f"x{i:02d}": (x >> i) & 1 for i in range(c)} |
        {f"y{i:02d}": (y >> i) & 1 for i in range(c)}
    )
    for w in e:
        o, a, b = g[s.get(w, w)]  # Getting the operation and operands
        if o == "AND":
            v[w] = v[a] & v[b]
        elif o == "OR":
            v[w] = v[a] | v[b]
        elif o == "XOR":
            v[w] = v[a] ^ v[b]
    
    for i in range(c + 1):
        if v[f"z{i:02d}"] != ((x + y) >> i) & 1:
            test1_cache[cache_key] = i
            return i
    test1_cache[cache_key] = c + 1
    return c + 1

# Test function for finding minimum test error with memoization
def testn(s):
    # Use a cache to store results of testn function
    cache_key = tuple(s.items())
    if cache_key in testn_cache:
        return testn_cache[cache_key]
    
    try:
        e = [
            w for w in graphlib.TopologicalSorter(
                {s.get(w, w): {a, b} for w, (o, a, b) in g.items()}
            ).static_order() if w in g
        ]
        result = min(
            test1(e, x, y, s)
            for x, y in ((m, 0), (0, m), (m, 1), (1, m), (m, m))
        )
        testn_cache[cache_key] = result
        return result
    except graphlib.CycleError:
        testn_cache[cache_key] = 0
        return 0

# Start solving the problem
s = {}
while len(s) < 8:
    a, b = max(
        ((a, b) for a in g for b in g if a < b and a not in s and b not in s),
        key=lambda p: testn(s | {p[0]: p[1], p[1]: p[0]})
    )
    s.update({a: b, b: a})

# Output the sorted result of wires that were updated
swapped_wires = ",".join(sorted(s))
print("Part 2:", swapped_wires)

# Print the elapsed time
print(time.time() - start_time)