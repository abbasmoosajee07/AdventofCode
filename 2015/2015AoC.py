import re
import numpy as np
import os
from pathlib import Path

# Define the directory and file name
directory = r'C:\Users\User\Documents\AdventofCode\2015\DataFiles'
test = os.path.abspath("DataFiles")

file_name = 'Day6_lights.txt'

# Create the full file path
file_path1 = os.path.join(test, file_name)
file_path = os.path.join(directory, file_name)

print(file_path1)
print(file_path)

# # Now you can open the file
# with open(file_path1) as file:
#     lights_inst = file.read()

# print(lights_inst)


# Get the current folder path
current_directory = os.getcwd()

# Set the working directory to the current folder
os.chdir(current_directory)

# Confirm the working directory is now set to the current folder
print("Working Directory Set To:", os.getcwd())
