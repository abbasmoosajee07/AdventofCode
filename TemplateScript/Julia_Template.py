
#!/usr/bin/env python3

import os, time

def create_julia_script(day=1, year=2024, author='your name', header_text = "Test"):
    """
    Sets up the folder structure, Julia script, and input file for an Advent of Code challenge.

    Parameters:
        day (int): Day of the challenge.
        year (int): Year of the challenge.
        author (str): Author name to include in the generated Julia script.

    Returns:
        None
    """
    # Zero-pad the day for folder and filenames
    padded_day = str(day).zfill(2)

    # Define base directory and paths
    base_dir = os.path.join(str(year), padded_day)
    julia_file_path = os.path.join(base_dir, f'{year}Day{padded_day}.jl')

    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Create Julia script if it doesn't already exist
    if not os.path.exists(julia_file_path):
        current_time = time.localtime()
        month = time.strftime('%b', current_time)
        script_content = f'''#=
{header_text}=#

#!/usr/bin/env julia

using Printf, DelimitedFiles

# Load the input data from the specified file path
const D{padded_day}_FILE = "Day{padded_day}_input.txt"
const D{padded_day}_FILE_PATH = joinpath(dirname(@__FILE__), D{padded_day}_FILE)

# Read the input data
input_data = readlines(D{padded_day}_FILE_PATH)
println(input_data)

'''
        with open(julia_file_path, 'w') as julia_file:
            julia_file.write(script_content)
        print(f"Created Julia script '{julia_file_path}'.")
    else:
        print(f"Julia script '{julia_file_path}' already exists.")
