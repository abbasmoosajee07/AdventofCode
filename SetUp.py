import os 
import sys

import numpy as np
import matplotlib.pyplot as plt

# Enable interactive mode
# plt.ion()

# Generate test data using numpy
x = np.linspace(0, 10, 100)  # 100 points from 0 to 10
y = np.sin(x) + np.random.normal(0, 0.1, 100)  # Sine wave with some noise

# Create a plot using matplotlib
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Noisy Sine Wave', color='b', marker='o', markersize=4, linestyle='--')
plt.title('Test Plot: Noisy Sine Wave')
plt.xlabel('X-axis (0 to 10)')
plt.ylabel('Y-axis (sin(x) + noise)')
plt.legend()
plt.grid(True)
plt.show()  # Display the plot inline in VS Code's interactive window



def read_file_in_script_directory(filename):
    # Get the script directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Set the working directory to the script's directory
    os.chdir(script_directory)
    
    # Construct the full file path
    file_path = os.path.join(script_directory, filename)

    
    # Read and return the file content
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"Error: {filename} not found in {script_directory}"

