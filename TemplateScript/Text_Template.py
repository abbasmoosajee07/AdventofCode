import os, time

def create_txt_file(day=1, year=2024, author='your name'):
    """
    Creates a .txt file for the Advent of Code challenge.

    Parameters:
        day (int): The day of the challenge (default is 6).
        year (int): The year of the challenge (default is 2022).
        author (str): The author of the solution (default is "abbasmoosajee07").

    Returns:
        None
    """
    # Zero-pad the day for filenames
    padded_day = str(day).zfill(2)

    # Define base directory and paths
    base_dir = os.path.join(str(year), padded_day)
    txt_file_path = os.path.join(base_dir, f'Day{padded_day}_input.txt')

    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Check if the text file already exists
    if not os.path.exists(txt_file_path):
        # Create the content for the text file
        current_time = time.localtime()
        month = time.strftime('%b', current_time)
        file_content = f''''''

        # Write the content to the file
        with open(txt_file_path, 'w') as txt_file:
            txt_file.write(file_content)

        print(f"Created text file '{txt_file_path}'.")
    else:
        print(f"Text file '{txt_file_path}' already exists.")
