"""Advent of Code - Day 4, Year 2025
Solution Started: December 4, 2025
Puzzle Link: https://adventofcode.com/2025/day/4
Solution by: Abbas Moosajee
Brief: [Code/Problem Description]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "Day04_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class Printers:
    ADJACENT = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    def __init__(self, input_grid):
        self.grid_dict = {
            (row_no, col_no): cell
            for row_no, row_data in enumerate(input_grid)
            for col_no, cell in enumerate(row_data)
        }

    def get_neighbors(self, pos):
        paper_neighbors = set()
        for (dr, dc) in self.ADJACENT:
            new_pos = (pos[0] + dr, pos[1] + dc)
            if self.grid_dict.get(new_pos, '.') == '@':
                paper_neighbors.add(new_pos)
        return paper_neighbors

    def get_paper_rolls(self):
        return set(filter(lambda item: item[1] == '@', self.grid_dict.items()))

    def identify_accescible_paper(self):
        accescible_rolls = 0
        for pos, cell in self.grid_dict.items():
            if cell != '@':
                continue
            papers = self.get_neighbors(pos)
            if len(papers) < 4:
                accescible_rolls += 1
        return accescible_rolls

    def move_all_papers(self):
        init_papers = len(self.get_paper_rolls())
        while True:
            accescible_rolls = 0
            for pos, cell in self.grid_dict.items():
                if cell != '@':
                    continue
                papers = self.get_neighbors(pos)
                if len(papers) < 4:
                    accescible_rolls += 1
                    self.grid_dict[pos] = '.'
            if accescible_rolls == 0:
                break

        return init_papers - len(self.get_paper_rolls())

aoc_print = Printers(data)
papers_avail = aoc_print.identify_accescible_paper()
print("AoC Day 04, P1:", papers_avail)

papers_moved = aoc_print.move_all_papers()
print("AoC Day 04, P2:", papers_moved)