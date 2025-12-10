"""Advent of Code - Day 10, Year 2025
Solution Started: December 10, 2025
Puzzle Link: https://adventofcode.com/2025/day/10
Solution by: Abbas Moosajee
Brief: [Factory]"""

#!/usr/bin/env python3
import re
from pathlib import Path
from z3 import Int, Optimize, sat
from collections import deque, Counter

# Load input file
input_file = "Day10_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class AOC_Factory:
    def __init__(self, factory_info):
        self.factory_info = factory_info

    def parse_data(self, machine):
        # Extract groups by bracket type
        square = re.findall(r'\[.*?\]', machine)[0].strip("[]")
        square_bin = []
        for light in square:
            light_val = 0
            if light == '#':
                light_val = 1
            square_bin.append(light_val)

        rounds = [tuple(map(int, x.strip("()").split(",")))
                    for x in re.findall(r'\(.*?\)', machine)]

        curly = list(map(int, re.findall(r'\{(.*?)\}', machine)[0].split(",")))
        return tuple(square_bin), rounds, curly

    def match_lights(self):
        total_presses = 0
        for machine_no, machine_data in enumerate(self.factory_info[:]):
            target_lights, schematics, _ = self.parse_data(machine_data)
            init_lights = [0] * len(target_lights)
            queue = deque(([press], init_lights) for press in schematics)
            visited = set()
            while queue:
                buttons_hist, current_lights = queue.popleft()
                press_now = buttons_hist[-1]
                button_set = tuple(sorted(buttons_hist))
                if button_set in visited:
                    continue
                visited.add(button_set)
                new_lights = current_lights.copy()
                for press in press_now:
                    new_lights[press] = 1 - current_lights[press]
                if tuple(new_lights) == target_lights:
                    # print(machine_no, len(buttons_hist))
                    total_presses += len(buttons_hist)
                    break
                for next_button in schematics:
                    if next_button == press_now:
                        continue
                    queue.append((buttons_hist + [next_button], new_lights.copy()))
        return total_presses

    def match_joltage_basic(self):
        total_presses = 0
        for machine_no, machine_data in enumerate(self.factory_info[:]):
            _, schematics, target_jolts = self.parse_data(machine_data)
            init_jolts = [0] * len(target_jolts)
            queue = deque(([press], init_jolts) for press in schematics)
            visited = set()
            while queue:
                buttons_hist, current_jolts = queue.popleft()
                press_now = buttons_hist[-1]
                button_set = tuple(sorted(buttons_hist))
                if button_set in visited:
                    continue
                visited.add(button_set)
                new_jolts = current_jolts.copy()
                for press in press_now:
                    new_jolts[press] += 1
                if tuple(new_jolts) == target_jolts:
                    print(machine_no, len(buttons_hist))
                    total_presses += len(buttons_hist)
                    break
                for next_button in schematics:
                    if next_button == press_now:
                        continue
                    queue.append((buttons_hist + [next_button], new_jolts.copy()))
        return total_presses

    def match_joltage_with_z3(self):
        total_presses = 0

        for machine_no, machine_data in enumerate(self.factory_info):
            _, schematics, target_jolts = self.parse_data(machine_data)

            # Normalize target and get number of slots
            n_slots = len(target_jolts)

            # Build delta vectors: for each schematic press, how much it increments each slot
            deltas = []
            for press in schematics:
                # press may be something like (1,3) or [2] etc.
                c = Counter(press)
                vec = [c[i] for i in range(n_slots)]
                deltas.append(vec)

            # Create z3 Int variables: count_p >= 0 for each schematic
            num_presses = len(deltas)
            counts = [Int(f"c_{i}") for i in range(num_presses)]

            opt = Optimize()

            # Non-negativity constraints (counts are integers >= 0)
            for v in counts:
                opt.add(v >= 0)

            # For each slot i: sum_j (deltas[j][i] * counts[j]) == target[i]
            for i in range(n_slots):
                opt.add(sum(deltas[j][i] * counts[j] for j in range(num_presses)) == target_jolts[i])

            # Minimize total presses
            total_var = sum(counts)
            opt.minimize(total_var)

            # Check and extract model
            if opt.check() == sat:
                m = opt.model()
                # sum up counts as integers
                machine_total = sum(m[v].as_long() for v in counts)
                # print(machine_no, machine_total)
                total_presses += machine_total
            else:
                # unsatisfiable: no combination of schematic presses reaches target
                print(machine_no, "UNSAT")
                # you can decide to raise or skip; here we skip adding presses

        return total_presses


factory = AOC_Factory(data)
print("AOC Day 10, P1:", factory.match_lights())
print("AOC Day 10, P2:", factory.match_joltage_with_z3())