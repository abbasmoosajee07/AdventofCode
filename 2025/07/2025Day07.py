"""Advent of Code - Day 7, Year 2025
Solution Started: December 7, 2025
Puzzle Link: https://adventofcode.com/2025/day/7
Solution by: Abbas Moosajee
Brief: [Laboratories]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import deque

# Load input file
input_file = "Day07_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class AOC_LABS:
    def __init__(self, init_map):
        self.map_dict = {
            (row_no, col_no): cell
            for row_no, row_data in enumerate(init_map)
            for col_no, cell in enumerate(row_data)
        }
        self.start_pos = next(pos for pos, cell in self.map_dict.items() if cell == 'S')

    def count_splits(self):
        queue = deque([self.start_pos])
        visited = set()
        split_count = 0
        while queue:
            beam_pos = queue.popleft()
            beam_row, beam_col = beam_pos
            if beam_pos in visited:
                continue
            visited.add(beam_pos)
            map_cell = self.map_dict.get(beam_pos, ' ')
            if map_cell in '.S':
                new_beam = beam_row + 1, beam_col
                queue.appendleft(new_beam)
            elif map_cell == '^':
                split_count += 1
                right_beam = beam_row, beam_col + 1
                left_beam = beam_row, beam_col - 1
                queue.appendleft(right_beam)
                queue.appendleft(left_beam)
        return split_count

    def build_timelines(self):
        queue = deque([[self.start_pos]])
        total_timelines = set()
        while queue:
            beam_path = queue.popleft()
            beam_row, beam_col = beam_path[-1]
            map_cell = self.map_dict.get((beam_row, beam_col), 'NA')
            if map_cell in '.S':
                new_beam = beam_row + 1, beam_col
                queue.appendleft(beam_path + [new_beam])
            elif map_cell == '^':
                right_beam = beam_row, beam_col + 1
                left_beam = beam_row, beam_col - 1
                queue.appendleft(beam_path +[right_beam])
                queue.appendleft(beam_path + [left_beam])
            elif map_cell == 'NA':
                total_timelines.add(tuple(beam_path))
        return len(total_timelines)

    def count_timelines_memoized(self):
        """Memoized DFS - fastest for maps with overlapping subproblems."""
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def count_from(pos, depth=0, max_depth=1000):
            """Count paths from position to outside map."""
            if depth > max_depth:
                return 0  # Prevent infinite recursion

            cell = self.map_dict.get(pos)
            if cell is None:
                return 1  # Reached outside - one timeline

            if cell in '.S':
                return count_from((pos[0] + 1, pos[1]), depth + 1)
            elif cell == '^':
                left = count_from((pos[0], pos[1] - 1), depth + 1)
                right = count_from((pos[0], pos[1] + 1), depth + 1)
                return left + right
            return 0

        return count_from(self.start_pos)


labs = AOC_LABS(data)
print("AOC Day 07, P1:", labs.count_splits())
print("AOC Day 07, P2:", labs.count_timelines_memoized())