"""Advent of Code - Day 9, Year 2025
Solution Started: December 9, 2025
Puzzle Link: https://adventofcode.com/2025/day/9
Solution by: Abbas Moosajee
Brief: [Movie Theater]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "Day09_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class Movie_Theatre:
    def __init__(self, seat_list):
        self.all_seats = [tuple(map(int, seat_info.split(","))) for seat_info in seat_list]

    def find_largest_rectangle(self):
        largest_area = 0
        for seat_1 in self.all_seats:
            for seat_2 in self.all_seats:
                if seat_1 == seat_2:
                    continue
                height = abs(seat_2[0] - seat_1[0]) + 1
                width = abs(seat_2[1] - seat_1[1]) + 1
                rect_area = height * width
                largest_area = max(largest_area, rect_area)
        return largest_area

    def restricted_rectangle(self):
        # Parse points
        points = self.all_seats

        # Build consecutive line segments (closed loop)
        lines = []
        n = len(points)
        for i in range(n):
            from_i = points[i]
            i_to = points[(i + 1) % n]
            lines.append((from_i, i_to))

        largest_rect = 0

        # Check all point pairs
        for r1, c1 in points:
            for r2, c2 in points:
                if r1 == r2 and c1 == c2:
                    continue

                # interior rectangle bounds
                min_row = min(r1, r2) + 1
                max_row = max(r1, r2) - 1
                min_col = min(c1, c2) + 1
                max_col = max(c1, c2) - 1

                valid = True

                for (fr, fc), (tr, tc) in lines:

                    # (first direction)
                    if (fr >= min_row and tr <= max_row and
                        fc >= min_col and tc <= max_col):
                        valid = False
                        break

                    # (reverse direction)
                    if (tr >= min_row and fr <= max_row and
                        tc >= min_col and fc <= max_col):
                        valid = False
                        break

                if valid:
                    height = abs(r1 - r2) + 1
                    width =  abs(c1 - c2) + 1
                    largest_rect = max(largest_rect, height * width)

        return largest_rect

movie = Movie_Theatre(data)
print("AOC Day 09, P1:", movie.find_largest_rectangle())
print("AOC Day 09, P2:", movie.restricted_rectangle())