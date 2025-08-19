"""Advent of Code - Day 22, Year 2022
Solution Started: Dec 11, 2024
Puzzle Link: https://adventofcode.com/2022/day/22
Solution by: abbasmoosajee07
Brief: [Moving in a non-square Grid]
"""
import os, subprocess
# File paths
solution_p1 = "2022Day22_P1.py"
solution_path_p1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p1)

solution_p2 = "2022Day22_P2.py"
solution_path_p2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), solution_p2)

# Run Python script
subprocess.run(["python", solution_path_p1], check=True)

# Run Ruby script
subprocess.run(["python", solution_path_p2], check=True)

