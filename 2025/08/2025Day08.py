"""Advent of Code - Day 8, Year 2025
Solution Started: December 8, 2025
Puzzle Link: https://adventofcode.com/2025/day/8
Solution by: Abbas Moosajee
Brief: [Playground]"""

#!/usr/bin/env python3
from pathlib import Path
from math import sqrt, prod
from itertools import combinations

# Load input file
input_file = "Day08_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()
# -------------------------
# Union–Find (Disjoint Set)
# -------------------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

class JunctionBox:
    def __init__(self, box_coords):
        self.boxes = [tuple(map(int, coords.split(","))) for coords in box_coords]

    @staticmethod
    def euclid_dist(pos_1, pos_2):
        x1, y1, z1 = pos_1
        x2, y2, z2 = pos_2
        sqr_dist = (x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2
        return sqrt(sqr_dist)

    def build_circuits(self, max_k = 1000):
        boxes = self.boxes

        uf = UnionFind(len(boxes))

        part_1 = part_2 = 0
        merges = 0

        pairs = [(test_pair) for test_pair in combinations(list(enumerate(boxes)), 2)]

        pairs.sort(key=lambda c: self.euclid_dist(c[0][1], c[1][1]))

        for k, pair in enumerate(pairs):
            if k == max_k:

                comp_size = [0] * len(boxes)
                for i in range(len(boxes)):
                    comp_size[uf.find(i)] += 1

                comp_size.sort(reverse=True)
                part_1 = prod(comp_size[:3])

            if uf.union(pair[0][0], pair[1][0]):
                merges += 1

            if merges == len(boxes) - 1:
                part_2 = pair[0][1][0] * pair[1][1][0]
                break

        return part_1, part_2


junction = JunctionBox(data)
part_1, part_2 = junction.build_circuits()
print("AOC Day 08, P1:", part_1)
print("AOC Day 08, P2:", part_2)


