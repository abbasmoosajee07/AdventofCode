import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting capabilities
from pathlib import Path

def get_repository_path():
    """
    Returns the absolute Path to the repository's root directory.
    Assumes the script is located inside the repository.
    """
    # Get the path of the current file using Pathlib
    current_file_path = Path(__file__).resolve()
    
    # Move up the directory tree as needed
    # Adjust the number of parents based on your repository structure
    repo_path = current_file_path.parent.parent
    
    return repo_path

def parse_runtime_file(file_path, year):
    """
    Parses a single runtime file and extracts data into a structured format.
    """
    try:
        with file_path.open('r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []
    
    # Skip headers and table border
    data = []
    start_end = [(i + 1) for i, line in enumerate(lines) if line.strip() == "-" * len(line.strip())]
    
    if len(start_end) < 2:
        print(f"Invalid table format in file: {file_path}")
        return []
    
    for line in lines[start_end[0]:start_end[1]]:
        if not line.strip() or line.strip().startswith('-'):
            continue
        
        parts = line.split()
        
        # Ensure the row has enough data
        if len(parts) < 8:
            continue
        
        try:
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
        except (ValueError, IndexError) as e:
            print(f"Error parsing line in {file_path}: {line.strip()}")
            continue
    
    return data

def read_all_runtime_tables(base_folder):
    """
    Traverses all yearly folders and combines data from all runtime tables.
    Looks for data in the 'analysis' subfolder of each year folder.
    """
    all_data = []
    base_path = Path(base_folder)

    if not base_path.exists():
        print(f"Base folder does not exist: {base_path}")
        return pd.DataFrame()

    # Use glob to find all year folders
    for year_path in base_path.glob('*'):
        if year_path.is_dir():
            try:
                year = int(year_path.name)  # Assuming folder names are years
            except ValueError:
                continue  # Skip non-numeric folder names

            # Look for the analysis subfolder
            analysis_folder = year_path / 'analysis'
            if not analysis_folder.exists():
                print(f"Analysis folder not found in {year_path}")
                continue

            # Find all results files in the analysis folder
            for results_file in analysis_folder.glob('*_results.txt'):
                year_data = parse_runtime_file(results_file, year)
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
    bars = ax.bar(summary['Year'], summary['Total_Time']/1000, color=colors, edgecolor='black', zorder=2)

    # Add color bar for Total_memory
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
    sm.set_array([])  # Required for ScalarMappable
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Total Memory')

    # Add labels and title
    ax.set_title('Advent of Code: Yearly Summary')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Time (s)')
    ax.set_xticks(summary['Year'])
    ax.set_xticklabels(summary['Year'])

    ax.grid(visible=True, which='major', color='grey', axis='y', linestyle='--', linewidth=0.7, alpha=0.9, zorder=1)

    # Show plot
    plt.tight_layout()

    # Save the plot to the script's directory using pathlib
    script_location = Path(__file__).parent
    plot_filename = script_location / 'overall_summary.png'
    plt.savefig(plot_filename)
    print(f"Plot saved to {plot_filename}")
    plt.show()
    
    return summary  # Return the summary DataFrame

# Example usage
summary_df = annual_summary(combined_data)

# Filter rows where Avg_ms is greater than or equal to 30,000
over_15s = combined_data.loc[combined_data['Avg_ms'] >= 15_000, ['Year', 'Day', 'Avg_ms']]

# Save the filtered data to a text file (tab-separated) using pathlib
output_file = Path(__file__).parent / "problems_over_15s.txt"
over_15s.to_csv(output_file, sep="\t", index=False)

# Print the filtered data to the console
print(over_15s)