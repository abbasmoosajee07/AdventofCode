# Advent of Code - Day 15, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/15
# Solution by: [abbasmoosajee07]
# Brief: [Goblins vs Elves DnD]

import os
from typing import NamedTuple
from dataclasses import dataclass
import enum, collections, itertools

# Load the input data from the specified file path
D15_file = "Day15_input.txt"
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

# Representing positions as NamedTuples
class Pt(NamedTuple):
    x: int
    y: int
    
    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    @property
    def nb4(self):
        # Return four adjacent directions (right, left, down, up)
        return [self + d for d in [Pt(0, 1), Pt(1, 0), Pt(0, -1), Pt(-1, 0)]]

# Enum for team types (ELF and GOBLIN)
class Team(enum.Enum):
    ELF = enum.auto()
    GOBLIN = enum.auto()

# Define the Unit class that represents each player (Elf or Goblin)
@dataclass
class Unit:
    team: Team
    position: Pt
    hp: int = 200
    alive: bool = True
    power: int = 3

# Custom exception when an Elf dies
class ElfDied(Exception):
    pass

# Grid class to represent the game state
class Grid(dict):
    def __init__(self, lines, power=3):
        super().__init__()
        self.units = []

        # Initialize the grid and place units (Elves and Goblins)
        for i, line in enumerate(lines):
            for j, el in enumerate(line):
                self[Pt(i, j)] = el == '#'  # Wall positions
                if el in 'EG':
                    self.units.append(Unit(
                        team={'E': Team.ELF, 'G': Team.GOBLIN}[el],
                        position=Pt(i, j),
                        power={'E': power, 'G': 3}[el]
                    ))

    def play(self, elf_death=False):
        rounds = 0
        while True:
            if self.round(elf_death=elf_death):
                break
            rounds += 1
        return rounds * sum(unit.hp for unit in self.units if unit.alive)

    def round(self, elf_death=False):
        # Sort units by position (reading order)
        for unit in sorted(self.units, key=lambda unit: unit.position):
            if unit.alive:
                if self.move(unit, elf_death=elf_death):
                    return True

    def move(self, unit, elf_death=False):
        # Identify all target enemies (opposite team)
        targets = [target for target in self.units if unit.team != target.team and target.alive]
        occupied = {u2.position for u2 in self.units if u2.alive and unit != u2}

        if not targets:
            return True

        # Find all in-range squares for movement
        in_range = {pt for target in targets for pt in target.position.nb4 if not self[pt] and pt not in occupied}

        if unit.position not in in_range:
            move = self.find_move(unit.position, in_range)
            if move:
                unit.position = move

        # Check if any opponent is in range for combat
        opponents = [target for target in targets if target.position in unit.position.nb4]
        if opponents:
            target = min(opponents, key=lambda unit: (unit.hp, unit.position))
            target.hp -= unit.power

            if target.hp <= 0:
                target.alive = False
                if elf_death and target.team == Team.ELF:
                    raise ElfDied()

    def find_move(self, position, targets):
        # Perform BFS to find the shortest path to a target
        visiting = collections.deque([(position, 0)])
        meta = {position: (0, None)}
        seen = set()
        occupied = {unit.position for unit in self.units if unit.alive}

        while visiting:
            pos, dist = visiting.popleft()
            for nb in pos.nb4:
                if self[nb] or nb in occupied:
                    continue
                if nb not in meta or meta[nb] > (dist + 1, pos):
                    meta[nb] = (dist + 1, pos)
                if nb in seen:
                    continue
                if not any(nb == visit[0] for visit in visiting):
                    visiting.append((nb, dist + 1))
            seen.add(pos)

        try:
            min_dist, closest = min((dist, pos) for pos, (dist, parent) in meta.items() if pos in targets)
        except ValueError:
            return

        while meta[closest][0] > 1:
            closest = meta[closest][1]

        return closest


# Load the input data
lines = open(D15_file_path).read().splitlines()

# Initialize the grid and units
grid = Grid(lines)

# Part 1: Play the game and print the outcome
print('Part 1:', grid.play())

# Part 2: Try different elf powers until no elf dies
for power in itertools.count(4):
    try:
        outcome = Grid(lines, power).play(elf_death=True)
    except ElfDied:
        continue
    else:
        print('Part 2:', outcome)
        break

