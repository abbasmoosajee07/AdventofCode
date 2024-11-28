
#!/usr/bin/env python3

import os, time

def create_c_script(day=1, year=2024, author='your name', header_text = "Test"):
    """
    Sets up the folder structure, C script, and input file for an Advent of Code challenge.

    Parameters:
        day (int): Day of the challenge.
        year (int): Year of the challenge.
        author (str): Author name to include in the generated C script.

    Returns:
        None
    """
    # Zero-pad the day for folder and filenames
    padded_day = str(day).zfill(2)

    # Define base directory and paths
    base_dir = os.path.join(str(year), padded_day)
    c_file_path = os.path.join(base_dir, f'{year}Day{padded_day}.c')

    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Create C script if it doesn't already exist
    if not os.path.exists(c_file_path):
        current_time = time.localtime()
        month = time.strftime('%b', current_time)
        script_content = f'''/*
{header_text}*/

#include <stdio.h>
#include <stdlib.h>

// Define the input file name
#define INPUT_FILE "Day{padded_day}_input.txt"

// Function to read input file
void read_input(const char *filename) {{
    FILE *file = fopen(filename, "r");
    if (!file) {{
        perror("Unable to open file");
        exit(EXIT_FAILURE);
    }}
    
    char line[256];
    printf("Input data:\\n");
    while (fgets(line, sizeof(line), file)) {{
        printf("%s", line);
    }}
    
    fclose(file);
}}

// Main function
int main() {{
    printf("Advent of Code - Day {day}, Year {year}\\n");
    
    // Read input data
    read_input(INPUT_FILE);
    
    // Your solution logic goes here
    
    return 0;
}}
'''

        with open(c_file_path, 'w') as c_file:
            c_file.write(script_content)
        print(f"Created C script '{c_file_path}'.")
    else:
        print(f"C script '{c_file_path}' already exists.")