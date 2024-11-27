
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

# Define the path for the C script file
c_file_path = os.path.join(base_dir, f'{Year}Day{padded_day}.c')

# Check if the C script file already exists
if not os.path.exists(c_file_path):
    # Define the content of the C script with dynamic day and year
    c_script_content = f'''/* Advent of Code - Day {Day}, Year {Year}
 * Solution Started: {month} {day}, {year}
 * Puzzle Link: https://adventofcode.com/{Year}/day/{Day}
 * Solution by: {Author}
 * Brief: [Code/Problem Description]
 */

#include <stdio.h>
#include <stdlib.h>

// Define the input file path
#define INPUT_FILE "Day{padded_day}_input.txt"

// Function to read input data
void read_input(const char* file_path) {{
    FILE* file = fopen(file_path, "r");
    if (!file) {{
        perror("Error opening file");
        return;
    }}

    char line[256];
    printf("Input Data:\\n");
    while (fgets(line, sizeof(line), file)) {{
        printf("%s", line);
    }}

    fclose(file);
}}

int main() {{
    printf("Advent of Code - Day {Day}, Year {Year}\\n");
    printf("Reading input from %s\\n", INPUT_FILE);

    read_input(INPUT_FILE);

    // Solution logic goes here

    return 0;
}}
'''

    # Write the C script to the file
    with open(c_file_path, 'w') as file:
        file.write(c_script_content)
    print(f"Created C script '{Year}Day{padded_day}.c'.")
else:
    print(f"C script '{Year}Day{padded_day}.c' already exists.")

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
