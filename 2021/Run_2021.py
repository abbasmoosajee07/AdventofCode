# Advent of Code - 2021
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2021
# Solution by: [abbasmoosajee07]
# Brief: [Run all 2021 scripts]


#!/usr/bin/env python3
import os
from Benchmarks.execute_challenge import execute_challenge_scripts

if __name__ == "__main__":
    # Define constants
    YEAR = 2024
    CHALLENGE_NAME = 'Advent of Code'
    DAYS_TO_RUN = range(1, 26)
    COLOR_2024 = "#228B22"
    NUM_ITERATIONS = 3  # Number of iterations for benchmarking

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.abspath(script_dir)  # Repo directory (same level as script)
    base_dir = os.path.abspath(os.path.join(os.getcwd(), str(YEAR)))

    # Print repo directory for debugging purposes
    print(f"Repository Directory: {repo_dir}")

    # Execute the challenge scripts
    execute_challenge_scripts(CHALLENGE_NAME, YEAR, DAYS_TO_RUN, repo_dir, NUM_ITERATIONS, COLOR_2024)
