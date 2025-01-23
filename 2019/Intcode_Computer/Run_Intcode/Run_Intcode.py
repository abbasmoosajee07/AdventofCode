# Advent of Code - 2019
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2019
# Solution by: [abbasmoosajee07]
# Brief: [Run all 2019 scripts]

#!/usr/bin/env python3
import os
from Benchmarks.execute_challenge import execute_challenge_scripts

if __name__ == "__main__":
    # Define constants
    YEAR = 2019
    CHALLENGE_NAME = 'Intcode Challenges'
    DAYS_TO_RUN = (2, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23)
    INTCODE_COLOR = "#4B0082"
    NUM_ITERATIONS = 3  # Number of iterations for benchmarking

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.abspath(script_dir)  # Repo directory (same level as script)
    base_dir = os.path.abspath(os.path.join(os.getcwd(), str(YEAR)))

    # # Print repo directory for debugging purposes
    print(f"Repository Directory: {script_dir}")

    # Execute the challenge scripts
    execute_challenge_scripts(CHALLENGE_NAME, YEAR, DAYS_TO_RUN, base_dir, NUM_ITERATIONS, INTCODE_COLOR, script_dir)