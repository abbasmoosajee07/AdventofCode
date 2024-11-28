import os, time

def create_ruby_script(day=1, year=2024, author='your name', header_text = "Test"):
    """
    Sets up the folder structure, Ruby script, and input file for an Advent of Code challenge.

    Parameters:
        day (int): Day of the challenge.
        year (int): Year of the challenge.
        author (str): Author name to include in the generated Ruby script.

    Returns:
        None
    """
    # Zero-pad the day for folder and filenames
    padded_day = str(day).zfill(2)

    # Define base directory and paths
    base_dir = os.path.join(str(year), padded_day)
    ruby_file_path = os.path.join(base_dir, f'{year}Day{padded_day}.rb')

    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Create Ruby script if it doesn't already exist
    if not os.path.exists(ruby_file_path):
        current_time = time.localtime()
        month = time.strftime('%b', current_time)
        script_content = f'''=begin
{header_text}=end

require 'pathname'

# Define file name and extract complete path to the input file
D{padded_day}_file = "Day{padded_day}_input.txt"
D{padded_day}_file_path = Pathname.new(__FILE__).dirname + D{padded_day}_file

# Read the input data
input_data = File.readlines(D{padded_day}_file_path).map(&:strip)

# Main execution
if __FILE__ == $0
  puts "Advent of Code - Day {day}, Year {year}"
  puts {'input_data'}

  # Your solution logic goes here
end
'''

        with open(ruby_file_path, 'w') as ruby_file:
            ruby_file.write(script_content)
        print(f"Created Ruby script '{ruby_file_path}'.")
    else:
        print(f"Ruby script '{ruby_file_path}' already exists.")

