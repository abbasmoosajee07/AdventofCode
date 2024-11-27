
#!/usr/bin/env python3

import os, sys, time

# Default values for the arguments
DEFAULT_DAY = 1
DEFAULT_YEAR = 2022
DEFAULT_YEAR_SOLVE = 2024
DEFAULT_AUTHOR = 'abbasmoosajee07'

# Filter out unwanted arguments (e.g., those that come from Jupyter or IDE)
valid_args = [arg for arg in sys.argv if not arg.startswith('--')]

# Check if correct number of arguments are passed
if len(valid_args) < 2:
    print("Using default arguments:")
    print(f"Day: {DEFAULT_DAY}, Year: {DEFAULT_YEAR}, Year_Solve: {DEFAULT_YEAR_SOLVE}, Author: {DEFAULT_AUTHOR}")
    Day = DEFAULT_DAY
    Year = DEFAULT_YEAR
    Year_Solve = DEFAULT_YEAR_SOLVE
    Author = DEFAULT_AUTHOR
else:
    # Retrieve command line arguments, using defaults if any are missing
    Day = int(valid_args[1]) if len(valid_args) > 1 else DEFAULT_DAY
    Year = int(valid_args[2]) if len(valid_args) > 2 else DEFAULT_YEAR
    Year_Solve = int(valid_args[3]) if len(valid_args) > 3 else DEFAULT_YEAR_SOLVE
    Author = valid_args[4] if len(valid_args) > 4 else DEFAULT_AUTHOR

# Add zero padding to the day number for folder and filenames (but not the web link)
padded_day = str(Day).zfill(2)  # Pads day numbers to two digits (e.g., '01', '02')

# Define the path for the new subfolder using the padded day and year variables
base_dir = os.path.join(str(Year), padded_day)

# Get the current local time
current_time = time.localtime()
# Extract the time
month = time.strftime('%b', current_time)
day = current_time.tm_mday
year = current_time.tm_year

# Check if the subfolder already exists, if not, create it
if not os.path.exists(base_dir):
    os.makedirs(base_dir)
    print(f"Created subfolder '{padded_day}' in '{Year}'.")
else:
    print(f"Subfolder '{padded_day}' already exists in '{Year}'.")

# Define the path for the Julia script file
julia_file_path = os.path.join(base_dir, f'{Year}Day{padded_day}.jl')

# Check if the Julia script file already exists
if not os.path.exists(julia_file_path):
    # Define the content of the Julia script with dynamic day and year
    julia_script_content = f'''# Advent of Code - Day {Day}, Year {Year}
# Solution Started: {month} {day}, {year}
# Puzzle Link: https://adventofcode.com/{Year}/day/{Day}
# Solution by: [{Author}]
# Brief: [Code/Problem Description]

#!/usr/bin/env julia

using Printf, DelimitedFiles

# Load the input data from the specified file path
const D{padded_day}_FILE = "Day{padded_day}_input.txt"
const D{padded_day}_FILE_PATH = joinpath(dirname(@__FILE__), D{padded_day}_FILE)

# Read the input data
input_data = readlines(D{padded_day}_FILE_PATH)
println(input_data)

'''

    # Write the Julia script to the file
    with open(julia_file_path, 'w') as file:
        file.write(julia_script_content)
    print(f"Created Julia script '{Year}Day{padded_day}.jl'.")
else:
    print(f"Julia script '{Year}Day{padded_day}.jl' already exists.")

# Define the path for the input file
input_file_path = os.path.join(base_dir, f'Day{padded_day}_input.txt')

# Check if the input text file already exists
if not os.path.exists(input_file_path):
    # Create the empty input text file
    with open(input_file_path, 'w') as file:
        pass  # Just create an empty file
    print(f"Created empty input file 'Day{padded_day}_input.txt'.")
else:
    print(f"Input file 'Day{padded_day}_input.txt' already exists.")
