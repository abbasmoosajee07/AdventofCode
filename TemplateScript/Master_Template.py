
import sys, os
import time

# Import individual setup functions
from C_Template import create_c_script
from Julia_Template import create_julia_script
from Python_Template import create_python_script
from Ruby_Template import create_ruby_script
from Text_Template import create_txt_file

# Define default values for variables within the script
advent_day = 6
advent_year = 2022
author_name = "abbasmoosajee07"

# Define a dictionary for language options
language_script_create_functions = {
    "python": create_python_script,
    "c": create_c_script,
    "julia": create_julia_script,
    "ruby": create_ruby_script,
}

# Define the selected language/script type (change this variable as needed)
selected_language = "python"  # Choose between "python", "c", "julia", "ruby"
base_dir = os.path.join(str(advent_year))
print(os.path.dirname(os.path.abspath(__file__)))
def generate_header(day, year, author):
    """
    Generate the header for the script.

    Parameters:
        day (int): The day of the Advent of Code challenge.
        year (int): The year of the Advent of Code challenge.
        author (str): The name of the author.

    Returns:
        str: The formatted header string.
    """
    # Get current time
    current_time = time.localtime()
    month = time.strftime('%b', current_time)

    # Construct the header content
    header = f"""Advent of Code - Day {day}, Year {year}
Solution Started: {month} {current_time.tm_mday}, {current_time.tm_year}
Puzzle Link: https://adventofcode.com/{year}/day/{day}
Solution by: {author}
Brief: [Code/Problem Description]
"""
    return header

def main():
    """
    Main function to always run the txt setup and then the selected language setup.
    """
    # Always run the Txt File setup first
    print("\nSetup for Txt File script selected.")
    create_txt_file(day=advent_day, year=advent_year, author=author_name)

    # Map the selected language to the corresponding setup function
    language_create_function = language_script_create_functions.get(selected_language)

    if language_create_function:
        print(f"\nSetup for {selected_language.capitalize()} script selected.")
        
        # Generate header for the selected script
        header = generate_header(advent_day, advent_year, author_name)
        
        # Pass the generated header to the language setup function
        language_create_function(day=advent_day, year=advent_year, author=author_name, header_text=header)
    else:
        print(f"Error: No setup function found for {selected_language}. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
