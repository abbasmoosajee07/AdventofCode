# Advent of Code - 2024
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2024
# Solution by: [abbasmoosajee07]
# Brief: [Run all 2024 scripts]

#!/usr/bin/env python3
import os, subprocess, glob, time, sys, re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.cm import ScalarMappable

def get_file_line_count(file_path):
    """Get the number of lines in a script file."""
    try:
        with open(file_path, "r") as file:
            return len(file.readlines())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def generate_gradient_around_color(center_color, num_steps=10):
    """Create a gradient around the given center color."""
    center_rgb = mcolors.hex2color(center_color)
    lighter_colors = [tuple(min(1, c + i * 0.05) for c in center_rgb) for i in range(num_steps)]
    darker_colors = [tuple(max(0, c - i * 0.05) for c in center_rgb) for i in range(num_steps)]
    # Combine them to form a full gradient (darker -> center -> lighter)
    full_gradient = darker_colors[::-1] + [center_rgb] + lighter_colors
    return full_gradient[::-1]

def run_script(file_path):
    """Run a script based on its file extension and time its execution."""
    _, extension = os.path.splitext(file_path)
    file_name = os.path.basename(file_path)

    try:
        # Ignore unsupported files
        if extension in ['.txt', '.png', '.exe']:
            return None
        if file_name.startswith("Alt"):
            print(f"Skipping script: {file_name} (starts with 'Alt')")
            return None
        else:
            print(f"Running script: {file_name}")

        start_time = time.time()

        if extension == '.py':
            subprocess.run(['python', file_path], check=True, env={**os.environ, "SUPPRESS_PLOT": "1"})
        elif extension == '.c':
            executable = file_path.replace('.c', '')
            subprocess.run(['gcc', file_path, '-o', executable], check=True)
            subprocess.run([executable], check=True)
        elif extension == '.rb':
            subprocess.run(['ruby', file_path], check=True)
        elif extension == '.jl':
            subprocess.run(['julia', file_path], check=True)
        else:
            print(f"Unsupported file type for {file_name}. Skipping.")

        elapsed_time = time.time() - start_time
        print(f"Finished running {file_name} in {elapsed_time:.2f} seconds.")

        line_count = get_file_line_count(file_path)
        return extension, line_count, elapsed_time
    except subprocess.CalledProcessError as e:
        print(f"Error executing {file_name}: {e}")
        return None

def create_table(file_info, avg_times, times_taken, Year, repo_dir):
    """Generates a table summarizing iterations and statistics for available days, saves to a file, 
    and also creates a DataFrame for the data."""
    
    print("\nGenerating table...")

    # Determine maximum number of iterations
    max_iterations = max(len(iterations) for iterations in times_taken.values())

    # Prepare header for the table and DataFrame
    header = (
        ["Day"]
        + [f"Iter {i + 1}" for i in range(max_iterations)]
        + ["Avg(s)", "Total(s)", "% Rel", "Langs", "Lines"]
    )
    row_format = "{:<5}" + "{:<10}" * (len(header) - 1)

    # Initialize list to hold table rows and data for DataFrame
    table_lines = []
    df_data = []

    # Total time for percentage calculation
    total_time = sum(avg_times.values())
    total_line_count = 0
    total_iterations = np.array([])

    # Data for additional statistics
    all_avg_times = []

    # Add header to table_lines
    table_lines.append(row_format.format(*header))
    table_lines.append("-" * (len(header) * 10))  # Separator line

    # Fill table rows for only non-zero days
    for day, iterations in sorted(times_taken.items()):
        avg_time = avg_times.get(day, 0)
        if avg_time == 0:  # Skip days with zero average time
            continue

        iter_data = [f"{t:.2f}" for t in iterations]
        total_time_for_day = sum(iterations)  # Total time for this day
        percentage = (avg_time / total_time * 100) if total_time > 0 else 0
        lang, line_count = file_info.get(day, ("N/A", 0))

        # Collect data for DataFrame
        df_row = (
            [day]  # Day number
            + iterations  # Iteration times
            + [None] * (max_iterations - len(iterations))  # Empty for missing iterations
            + [avg_time, total_time_for_day, percentage, lang, line_count]
        )
        df_data.append(df_row)

        # Collect data for statistical analysis
        all_avg_times.append(avg_time)
        total_iterations = np.append(total_iterations, iterations)
        total_line_count += line_count

        # Prepare row for the text table
        row_data = (
            [f"{day:.2f}"]  # Day number
            + [f"{t:.2f}" for t in iterations]  # Iteration times
            + [""] * (max_iterations - len(iterations))  # Empty for missing iterations
            + [f"{avg_time:.2f}", f"{total_time_for_day:.2f}", f"{percentage:.2f}%", lang, f"{line_count:.2f}"]
        )
        table_lines.append(row_format.format(*row_data))

    # Calculate additional statistics for average times
    all_avg_times = np.array(all_avg_times)
    min_avg_time = np.min(all_avg_times)
    max_avg_time = np.max(all_avg_times)
    median_avg_time = np.median(all_avg_times)

    # Add an extra line for separation before the total row
    table_lines.append("-" * (len(header) * 10))  # Blank line before the total row for better separation

    # Calculate totals for each iteration and other stats
    iteration_totals = [f"{np.sum(total_iterations[i::max_iterations]):.2f}" for i in range(max_iterations)]

    # Ensure iteration_totals has the correct length
    if len(iteration_totals) < max_iterations:
        iteration_totals.extend([""] * (max_iterations - len(iteration_totals)))

    # Total row (sum of iteration times and line counts)
    total_row = (
        ["Total"]
        + iteration_totals  # Sum of each iteration across all days
        + [f"{total_time:.2f}", f"{sum([sum(iterations) for iterations in times_taken.values()]):.2f}", "100.00%", "N/A", f"{total_line_count:.2f}"]
    )
    
    # Add total row to table
    table_lines.append(row_format.format(*total_row))

    # Add blank line after the total row for better visual separation
    table_lines.append("")  # Another blank line after total row

    # Add statistical properties row for average times
    stats_row = [
        f"Total Time: {total_time:.2f} seconds",
        f"Average Time: {np.mean(all_avg_times):.2f} seconds",
        f"Median Time: {median_avg_time:.2f} seconds"
    ]
    
    table_lines.append("\n".join(stats_row))

    # Save to file (only the table)
    table_path = os.path.join(repo_dir, f"{Year}_RunTime_table.txt")
    with open(table_path, 'w') as f:
        for line in table_lines:
            f.write(line + "\n")

    print(f"Table saved to {table_path}")
    
        # Create DataFrame
    column_names = ["Day"] + [f"Iter {i+1}" for i in range(max_iterations)] + ["Avg(s)", "Total(s)", "% Rel", "Langs", "Lines"]
    df = pd.DataFrame(df_data, columns=column_names)

    # Add totals row to DataFrame
    totals_row = ["Total"] + iteration_totals + [total_time, sum([sum(iterations) for iterations in times_taken.values()]), 100.0, "N/A", total_line_count]
    df.loc[len(df)] = totals_row  # Append the totals row
    print(df)
    # Now, the dataframe is available as a variable
    return df

def create_plot(df, challenge, Year, center_color="#4CAF50"):
    # Remove the "Total" row (if it exists) to avoid plotting it
    df = df[df['Day'] != 'Total']

    # Convert the 'Day' column to numeric
    days = pd.to_numeric(df['Day'], errors='coerce')  # Convert days to numeric, coercing any errors to NaN
    avg_times = df['Avg(s)'].tolist()  # Get the average times for each day

    # Convert Iteration columns to numeric, handle errors by coercing to NaN
    iter_columns = [col for col in df.columns if col.startswith('Iter')]
    df[iter_columns] = df[iter_columns].apply(pd.to_numeric, errors='coerce')
    # iter_columns = [col for col in df.columns if col.startswith('Iter')]
    # df.loc[:, iter_columns] = df[iter_columns].apply(pd.to_numeric, errors='coerce')

    # # Get the iteration times for each day (Iter 1 to Iter 3)
    # iter_times = df[iter_columns].values
    # iter_times = np.nan_to_num(iter_times, nan=0)  # Replaces NaN with 0

    # # Calculate the standard deviation for each day based on iterations (Iter 1, Iter 2, Iter 3)
    # std_devs = np.std(iter_times, axis=1, ddof=0)  # Standard deviation for each day

    # Get the iteration times for each day (Iter 1 to Iter 3)
    iter_times = df[iter_columns].values

    # Calculate the standard deviation for each day based on iterations (Iter 1, Iter 2, Iter 3)
    std_devs = np.std(iter_times, axis=1, ddof=0)  # Standard deviation for each day

    # Handle the file info (langs and lines)
    file_info = dict(zip(df['Langs'], zip(df['Langs'], df['Lines'])))  # Create a dict of file info for Langs and Lines

    # Create a color gradient around the center color
    color_gradient = generate_gradient_around_color(center_color)
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_gradient", color_gradient)

    # Normalize the percentage values for color mapping
    total_time = np.sum(avg_times)  # Total time (sum of avg times)
    percentages = [(time / total_time) * 100 for time in avg_times]  # Percentage of total time for each day
    norm = mcolors.Normalize(vmin=min(percentages), vmax=max(percentages))
    bar_colors = [cmap(norm(p)) for p in percentages]

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(days, avg_times, color=bar_colors, zorder=3)

    # Set the y-axis limit
    max_y_value = max(avg_times)
    ax.set_ylim(0, max_y_value * 1.25)

    # Annotate the bars with file info (extension and line count)
    for i, (bar, percentage) in enumerate(zip(bars, percentages)):
        height = bar.get_height()
        label_position = height + 0.15
        file_path = df['Langs'].iloc[i]  # Get the file extension
        line_count = df['Lines'].iloc[i]  # Get the line count
        ax.text(bar.get_x() + bar.get_width() / 2, label_position,
                f"({file_path}) {line_count} lines", ha='center', va='bottom', fontsize=10, color='black', rotation=90)

    # Highlight max and min points
    max_day = days[np.argmax(avg_times)]  # Get the day with the max average time
    min_day = days[np.argmin(avg_times)]  # Get the day with the min average time
    max_time = np.max(avg_times)
    min_time = np.min(avg_times)
    ax.plot(max_day, max_time, 'rx', label=f"Max ({max_time:.2f}s)", markersize=5, zorder=5)
    ax.plot(min_day, min_time, 'bx', label=f"Min ({min_time:.2f}s)", markersize=5, zorder=5)

    # Add average and median lines
    average_time = np.mean(avg_times)  # Mean of the average times
    median_time = np.median(avg_times)  # Median of the average times
    ax.axhline(average_time, color='#008000', linestyle=':', label=f'Average: {average_time:.2f}s')
    ax.axhline(median_time, color='#800080', linestyle=':', label=f'Median: {median_time:.2f}s')

    # Add error bars based on the standard deviation for each day
    ax.errorbar(days, avg_times, yerr=std_devs, fmt='none', color='black', capsize=5, zorder=4)

    # Customize x-axis and y-axis labels
    ax.set_xticks(days)
    ax.set_xticklabels([f'Day {int(day)}' for day in days], rotation=45, ha='right')  # Ensure days are displayed as integers
    ax.set_ylabel("Average Time (seconds)", fontsize=14)
    ax.set_title(f'{challenge} Year {Year}: Total Time is {total_time:.2f} seconds', fontsize=18, fontweight='bold')

    # Add grid and legend
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, zorder=2)
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize=11, frameon=True, facecolor='white', edgecolor='black')

    # Make the plot layout tight
    plt.tight_layout()

    # Add a colorbar for the relative percentage
    cbar = plt.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax)
    cbar.set_label('Relative Percentage of Total Time (%)', fontsize=12)

    # Save and show the plot
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plot_path = os.path.join(script_dir, f"{Year}_RunTime_plot.png")
    plt.savefig(plot_path, bbox_inches='tight')
    plt.show()

    print(f"Plot saved to {plot_path}")

    # Return computed statistics
    return {
        'total_time': total_time,
        'min_time': min_time,
        'max_time': max_time,
        'average_time': average_time,
        'median_time': median_time,
        'std_dev_time': np.std(avg_times),  # standard deviation for avg_times
        'percentages': percentages,
        'max_day': max_day,
        'min_day': min_day
    }

def main(challenge, Year, days_to_run, num_iterations=5, center_color="#4CAF50"):
    """Main function to run scripts, aggregate stats over iterations, and generate overall results."""
    print(f"\n{challenge} - {Year}")
    print(f"Running scripts for days: {days_to_run} over {num_iterations} iterations.")

    repo_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir(repo_dir):
        print(f"Directory '{repo_dir}' does not exist.")
        return

    # Data structures for storing results
    times_taken = {day: [] for day in days_to_run}  # Store times for each day across iterations
    file_info = {}  # Store script info for each day
    avg_times = {}  # Initialize avg_times dictionary

    # Loop through iterations
    for iteration in range(num_iterations):
        print(f"\nIteration {iteration + 1}/{num_iterations}...")

        for day_dir in os.listdir(repo_dir):
            day_path = os.path.join(repo_dir, day_dir)
            if os.path.isdir(day_path) and day_dir.isdigit():
                day_number = int(day_dir)
                if day_number in days_to_run:
                    print(f"\nProcessing Day {day_number}...")
                    day_time, day_lines = 0, 0
                    languages = set()

                    # Execute all scripts for the day
                    for script_file in glob.glob(f"{day_path}/*"):
                        match = re.search(rf"{Year}Day(\d+)(?:_P\d+)?", os.path.basename(script_file))
                        script_day = int(match.group(1)) if match else None

                        if script_day == day_number:
                            result = run_script(script_file)
                            if result:
                                extension, line_count, elapsed_time = result
                                day_time += elapsed_time
                                day_lines += line_count
                                languages.add(extension[1:])  # Store language/extension without dot

                    # Collect results for this day
                    if day_time > 0:
                        languages_str = ", ".join(sorted(languages))
                        times_taken[day_number].append(day_time)  # Add this iteration's time
                        if day_number not in file_info:
                            file_info[day_number] = (f".{languages_str}", day_lines)

    # Calculate averages, skipping days with no recorded times
    for day, times in times_taken.items():
        if times:  # Ensure the list is not empty
            avg_times[day] = np.mean(times)
        else:
            avg_times[day] = 0  # Assign a default value for days with no data

    # Use averaged times for the table and plot
    run_df = create_table(file_info, avg_times, times_taken, Year, repo_dir)

    create_plot(run_df, challenge, Year, center_color)

    print(f"\nTotal script execution time over {num_iterations} iterations saved to table and plotted.")

if __name__ == "__main__":
    Year = 2024
    Challenge = 'Advent of Code'
    days_to_run = range(1, 26)
    color_2024 = "#673147"
    num_iterations = 5  # Number of iterations for benchmarking
    main(Challenge, Year, days_to_run, num_iterations, color_2024)
