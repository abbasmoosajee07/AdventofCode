import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting capabilities

def parse_runtime_file(file_path, year):
    """
    Parses a single runtime file and extracts data into a structured format.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Skip headers and table border
    data = []
    for line in lines[3:]:  # Start after the header
        if not line.strip():  # Skip empty lines
            continue
        parts = line.split()
        if len(parts) < 5:  # Ensure the row has enough data
            continue
        day, time, percentage, lang, *line_count = parts
        data.append({
            "Year": year,
            "Day": int(day),
            "Time (s)": float(time),
            "Percentage": float(percentage.strip('%')),
            "Language": lang,
            "Line Count": int(line_count[0])
        })
    return data

def read_all_runtime_tables(base_folder):
    """
    Traverses all yearly folders and combines data from all runtime tables.
    """
    all_data = []
    for year_folder in os.listdir(base_folder):
        year_path = os.path.join(base_folder, year_folder)
        if os.path.isdir(year_path):  # Check if it's a directory
            try:
                year = int(year_folder)  # Assuming folder names are years
            except ValueError:
                continue  # Skip non-numeric folder names
            for file_name in os.listdir(year_path):
                if file_name.endswith('_RunTime_table.txt'):
                    file_path = os.path.join(year_path, file_name)
                    all_data.extend(parse_runtime_file(file_path, year))
    return pd.DataFrame(all_data)

def analyze_data(dataframe):
    """
    Analyzes the combined runtime data and prints a summary.
    """
    if dataframe.empty:
        print("No data to analyze.")
        return
    
    # Summary by year
    summary = dataframe.groupby('Year').agg(
        Total_Time=('Time (s)', 'sum'),
        Average_Time=('Time (s)', 'mean'),
        Median_Time=('Time (s)', 'median'),
        Total_Lines=('Line Count', 'sum'),
        Average_Lines=('Line Count', 'mean')
    )
    print("Yearly Summary:")
    print(summary)
    
    # Find slowest and fastest days
    slowest = dataframe.sort_values('Time (s)', ascending=False).head(5)
    fastest = dataframe.sort_values('Time (s)').head(5)
    
    print("\nSlowest Days:")
    print(slowest)
    print("\nFastest Days:")
    print(fastest)

def plot_3d_runtime(dataframe):
    """
    Creates a 3D plot with:
    - X-axis: Days
    - Y-axis: Time (s)
    - Z-axis: Years
    """
    if dataframe.empty:
        print("No data to plot.")
        return

    # Prepare data for plotting
    x = dataframe['Year']  # Days
    y = dataframe['Day']  # Time in seconds
    z = dataframe['Time (s)']  # Years

    # Create 3D plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    scatter = ax.scatter(x, y, z, c=y, cmap='viridis', s=50)

    # Add labels and title
    ax.set_xlabel("Years")
    ax.set_ylabel("Days")
    ax.set_zlabel("Time (s)")
    ax.set_title("Advent of Code Runtime Analysis")
    ax.set_zlim(0, 60)

    # Add a color bar to indicate time scale
    cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label("Time (s)")

    # Show plot
    plt.show()
import numpy as np

def plot_3d_runtime(dataframe):
    """
    Creates a 3D bar plot with:
    - X-axis: Days
    - Y-axis: Years
    - Z-axis: Time (s)
    """
    if dataframe.empty:
        print("No data to plot.")
        return

    # Prepare data for plotting
    x = dataframe['Year']  # Days
    y = dataframe['Day']  # Time in seconds
    z = dataframe['Time (s)']  # Years

    # Get the unique days and years for plotting
    unique_days = np.unique(x)
    unique_years = np.unique(y)

    # Create a 2D grid for the years and days
    x_grid, y_grid = np.meshgrid(unique_days, unique_years)

    # Reshape the Z data to match the grid
    z_grid = np.full_like(x_grid, np.nan, dtype=float)
    for i in range(len(x)):
        day_index = np.where(unique_days == x[i])[0][0]
        year_index = np.where(unique_years == y[i])[0][0]
        z_grid[year_index, day_index] = z[i]

    # Create the plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Bar plot for the runtime
    for i in range(len(unique_years)):
        for j in range(len(unique_days)):
            if not np.isnan(z_grid[i, j]):
                ax.bar3d(x_grid[i, j], y_grid[i, j], 0, 1, 1, z_grid[i, j], color=plt.cm.viridis(z_grid[i, j] / max(z)), shade=True)

    # Set labels
    ax.set_xlabel('Years')
    ax.set_ylabel('Day')
    ax.set_zlabel('Time (s)')
    ax.set_title('Advent of Code Runtime Analysis')
    ax.set_zlim(0, 60)

    # Color bar to represent time
    mappable = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=z.min(), vmax=z.max()))
    mappable.set_array(z)
    cbar = fig.colorbar(mappable, ax=ax, pad=0.1)
    cbar.set_label('Time (s)')

    # Show plot
    plt.show()

def main():
    """
    Main function to execute the script.
    """
    # Get the directory where the script is located
    base_folder = os.path.dirname(os.path.abspath(__file__))
    print(f"Analyzing data from base folder: {base_folder}")
    
    # Read and combine all data
    combined_data = read_all_runtime_tables(base_folder)
    if combined_data.empty:
        print("No data found. Please check the file structure and paths.")
        return
    
    # Analyze the data
    analyze_data(combined_data)
    
    # Create the 3D plot
    plot_3d_runtime(combined_data)

if __name__ == "__main__":
    main()
