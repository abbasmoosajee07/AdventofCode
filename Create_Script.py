
import sys, os, time

# Import individual setup functions for each language
from Polyglot_Setups.Setup_C      import create_c_script
from Polyglot_Setups.Setup_Txt    import create_txt_file
from Polyglot_Setups.Setup_Ruby   import create_ruby_script
from Polyglot_Setups.Setup_Julia  import create_julia_script
from Polyglot_Setups.Setup_Python import create_python_script

# Define default values for the Advent of Code challenge
advent_day  = 21
advent_year = 2022
author_name = "abbasmoosajee07"
selected_language = "python"  # Options: "python", "c", "julia", "ruby"

# Dictionary mapping language names to their corresponding setup functions
language_script_create_functions = {
    "c"     : create_c_script,
    "ruby"  : create_ruby_script,
    "julia" : create_julia_script,
    "python": create_python_script,
}

# Get the directory of the current script
repo_dir = os.path.dirname(os.path.abspath(__file__))

def generate_header(day, year, author):
    """
    Generate the header for the script, including metadata and formatting.

    Parameters:
        day (int): The day of the Advent of Code challenge.
        year (int): The year of the Advent of Code challenge.
        author (str): The author's name.

    Returns:
        str: The formatted header string for the script.
    """
    # Get the current local time
    current_time = time.localtime()
    month = time.strftime('%b', current_time)  # Get abbreviated month name

    # Construct the header content for the script
    header = f"""Advent of Code - Day {day}, Year {year}
Solution Started: {month} {current_time.tm_mday}, {current_time.tm_year}
Puzzle Link: https://adventofcode.com/{year}/day/{day}
Solution by: {author}
Brief: [Code/Problem Description]
"""
    return header

def main():
    """
    Main function to orchestrate the creation of necessary files:
    - Always creates the .txt file first
    - Then creates the selected language-specific script.
    """
    print(f"\nAdvent of Code - Day {advent_day}, Year {advent_year}")

    # Always start by creating the text file setup
    print("\nSetting up Txt file...")
    create_txt_file(day=advent_day, year=advent_year, author=author_name, repo_dir=repo_dir)

    # Get the setup function for the selected language
    language_create_function = language_script_create_functions.get(selected_language)

    # If a valid setup function is found for the selected language, proceed
    if language_create_function:
        print(f"\nSetting up {selected_language.capitalize()} script...")

        # Generate the header content for the script
        header = generate_header(advent_day, advent_year, author_name)

        # Pass the header to the language-specific setup function to create the script
        language_create_function(day=advent_day, year=advent_year, author=author_name,
                                    header_text=header, repo_dir=repo_dir)
    else:
        # If no valid setup function is found, exit with an error message
        print(f"Error: No setup function found for {selected_language}. Exiting.")
        sys.exit(1)

    # Notify the user that all files were created
    print(f"\nAll necessary files have been created.")

if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
