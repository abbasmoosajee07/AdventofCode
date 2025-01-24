# Advent of Code - 2019
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2019
# Solution by: [abbasmoosajee07]
# Brief: [Benchmark Intcode]

import os, sys, time, copy, psutil
import pandas as pd
overal_start_time = time.time()

# Import the Intcode_CPU from the Intcode_Computer module in the parent directory
intcode_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(intcode_dir)
from Intcode_Computer import Intcode_CPU

# Define the path to the Benchmark_programs.txt file
benchmark_path = os.path.join(os.path.dirname(__file__), "Benchmark_programs.txt")

# Read and parse input data into a list of integers
with open(benchmark_path) as file:
    benchmark_programs = file.read().strip().split('\n')

# Initialize a DataFrame for storing benchmark results
benchmarks = pd.DataFrame()

def perform_benchmark(program, program_name, test_inputs):
    """
    Executes an Intcode program, measures its runtime, memory usage, and returns results as a DataFrame.
    """
    # Store original inputs to avoid modifying the test data
    og_inputs = copy.deepcopy(test_inputs)

    # Create the CPU instance and execute the program

    # Measure memory usage before starting
    process = psutil.Process()
    memory_before = process.memory_info().rss  # Memory in bytes before execution
    cpu = Intcode_CPU(program, init_inputs=test_inputs, debug=False)

    # Measure runtime
    start_time = time.time()
    cpu.process_program()
    end_time = time.time()

    # Measure memory usage after execution
    memory_after = process.memory_info().rss  # Memory in bytes after execution
    memory_used = memory_after - memory_before  # Difference in memory usage

    # Capture output and elapsed time
    output = cpu.get_result('output')
    elapsed_time = end_time - start_time

    # Create a local DataFrame for this test's results
    result_df = pd.DataFrame([{
        "Benchmark Prog": program_name,
        "Time (s)": f"{elapsed_time:.5f}s",
        "Memory(B)": memory_used,
        "Input": og_inputs,
        # "Output": output,

    }])

    return result_df

# Benchmarking programs ----------------------------------------

# Sum of primes: Sum of all primes up to the input
# requires O(n) memory.
# Example:
# Input: 10 => Output: 17
# Input: 2000000 => Output: 142913828922
sum_of_primes_program = list(map(int, benchmark_programs[0].split(',')))
result_prime_sum = perform_benchmark(sum_of_primes_program, "Sum of Primes", 100000)

# Ackermann function: Two-argument Ackermann function A(m, n)
# requires O(A(m, n)) memory
# Example:
# Input: 2, 4 => Output: 11
# Input: 3, 2 => Output: 29
ackermann_program = list(map(int, benchmark_programs[1].split(',')))
result_ackermann = perform_benchmark(ackermann_program, "Ackermann func", [3, 6])

# Integer square root: Integer square root of a non-negative number
# Example:
# Input: 16 => Output: 4
# Input: 130 => Output: 11
isqrt_program = list(map(int, benchmark_programs[2].split(',')))
result_isqrt = perform_benchmark(isqrt_program, "Int Sqaure Root", 130)

# Divmod: Quotient and remainder of Euclidean division a / b
# Example:
# Input: 1024, 3 => Output: 341, 1
# Input: 2842238103274937687216392838982374232734, 2384297346348274 => Output: 1192065288177262577484639, 768603395069648
divmod_program = list(map(int, benchmark_programs[3].split(',')))
result_divmod = perform_benchmark(divmod_program, "Divmod (Euclid)", [1024, 3])

# Factorization: Prime factorization of a number
# requires O(sqrt(n)) memory
# Example:
# Input: 399 => Output: 3, 7, 19
# Input: -1024 => Output: -1, then 2 ten times
# Input: 2147483647 => Output: 2147483647
# Input: 19201644899 => Output: 138569, 138571
factor_program = list(map(int, benchmark_programs[4].split(',')))
result_factor = perform_benchmark(factor_program, "Factorization", 399)

# Concatenate all results into the global DataFrame
benchmarks = pd.concat([benchmarks, result_prime_sum, result_ackermann, result_isqrt, result_divmod, result_factor], ignore_index=True)

# Optionally, print the final benchmarks DataFrame
print(benchmarks)

# Save the formatted table to a CSV or Excel file if needed
benchmarks.to_csv('benchmark_results.txt', sep="\t", index=False)

print(f"Total Benchmark Time = {time.time() - overal_start_time:.5f}s")

