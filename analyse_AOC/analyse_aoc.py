import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting capabilities

def get_repository_path():
    """
    Returns the absolute path to the repository's root directory.
    Assumes the script is located inside the repository.
    """
    # Get the path of the current file
    current_file_path = os.path.abspath(__file__)
    
    # Move up the directory tree as needed (e.g., assume repo is the parent directory)
    repo_path = os.path.abspath(os.path.join(current_file_path, os.pardir, os.pardir))
    
    return repo_path

def parse_runtime_file(file_path, year):
    """
    Parses a single runtime file and extracts data into a structured format.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Skip headers and table border
    data = []
    start_end = [(i + 1) for i, line in enumerate(lines) if line.strip() == "-" * len(line.strip())]

    for line in lines[start_end[0]:start_end[1]]:  # Start after the header and skip the last 4 lines (table border)
        if not line.strip():  # Skip empty lines
            continue
        parts = line.split()
        
        # Ensure the row has enough data
        if len(parts) < 8:
            continue
        
        # Assign values to variables
        day, avg_time, std_time, rel_time, avg_mb, std_mb, rel_mb, *Lang, file_size, Lines = parts
        
        # Append the row as a dictionary to the data list
        data.append({
            "Year": year,
            "Day": int(day),
            "Avg_ms": float(avg_time),
            "STD_ms": float(std_time),
            "rel_ms": float(rel_time.strip('%')),
            "Avg_mb": float(avg_mb),
            "STD_mb": float(std_mb),
            "rel_mb": float(rel_mb.strip('%')),
            "Lang": ' '.join(Lang),  # Join language(s) into a single string
            'Size_kb': float(file_size),
            "Lines": int(Lines)
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
                if file_name.endswith('_Run_Summary.txt'):
                    file_path = os.path.join(year_path, file_name)
                    year_data = parse_runtime_file(file_path, year)
                    all_data.extend(year_data)
    
    return pd.DataFrame(all_data)

def analyze_data(dataframe):
    """
    Analyzes the combined runtime data and prints a summary.
    """
    # Find slowest and fastest days
    slowest = dataframe.sort_values('Avg_ms', ascending=False).head(5)
    fastest = dataframe.sort_values('Avg_ms').head(5)
    
    print("\nSlowest Days:")
    print(slowest[['Year', 'Day', 'Avg_ms', 'STD_ms', 'Avg_mb', 'Lang']])
    
    print("\nFastest Days:")
    print(fastest[['Year', 'Day', 'Avg_ms', 'STD_ms', 'Avg_mb', 'Lang']])

# Example usage
repo_path = get_repository_path()
print(f"Repository path: {repo_path}")

# Read and combine all data
combined_data = read_all_runtime_tables(repo_path)
print(combined_data)
# Analyze the combined data
analyze_data(combined_data)

def annual_summary(dataframe):
    # Summary by year
    summary = dataframe.groupby('Year').agg(
        Total_Time=('Avg_ms', 'sum'),
        Average_Time=('Avg_ms', 'mean'),
        Median_Time=('Avg_ms', 'median'),
        Total_memory=('Avg_mb', 'sum'),
    ).reset_index()  # Reset index to make 'Year' a column

    print("Yearly Summary:")
    print(summary)

    # Normalize Total_memory for color mapping
    norm = plt.Normalize(summary['Total_memory'].min(), summary['Total_memory'].max())
    colors = plt.cm.viridis(norm(summary['Total_memory']))  # Using 'viridis' colormap

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bar plot with color scale
    bars = ax.bar(summary['Year'], summary['Total_Time']/1000, color=colors, edgecolor='black',zorder =2)

    # Add color bar for Total_memory
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
    sm.set_array([])  # Required for ScalarMappable
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Total Memory')

    # Add labels and title
    ax.set_title('Yearly Summary: Total Time with Total Lines as Color Scale')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Time (s)')
    ax.set_xticks(summary['Year'])
    ax.set_xticklabels(summary['Year'])

    ax.grid(visible=True, which='major', color ='grey', axis='y', linestyle='--', linewidth=0.7, alpha=0.9,zorder =1)

    # Show plot
    plt.tight_layout()


    # Save the plot to the script's directory
    script_location = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    plot_filename = os.path.join(script_location, 'overall_summary.png')  # Define the plot filename
    plt.savefig(plot_filename)  # Save the plot as a PNG file
    print(f"Plot saved to {plot_filename}")
    plt.show()
    return summary  # Return the summary DataFrame

# Example usage
summary_df = annual_summary(combined_data)

over_30s = combined_data.loc[combined_data['Avg_ms'] >= 30_000, ['Year', 'Day', 'Avg_ms']]
over_30s.to_csv("problems_over_30s.txt", sep="\t", index=False)

print(over_30s)
