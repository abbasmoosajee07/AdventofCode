# Advent of Code - Day 1, Year 2022
# Solution Started: Nov 27, 2024
# Puzzle Link: https://adventofcode.com/2022/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Cookies and Calories]

#!/usr/bin/env julia

using Printf, DelimitedFiles

# Load the input data from the specified file path
const D01_FILE = "Day01_input.txt"
const D01_FILE_PATH = joinpath(dirname(@__FILE__), D01_FILE)

# Read the input data
input_data = readlines(D01_FILE_PATH)

# Split the data by double newlines (to get blocks of data)
blocks = split(join(input_data, "\n"), "\n\n")

# Now, split each block into numbers (by splitting on newline) and parse to integers
cookie_list = [[parse(Int, num) for num in split(block, "\n") if !isempty(num)] for block in blocks]

max_calories = maximum(map(sum, cookie_list))

println("Part 1:", max_calories)

total_calories = []
for sub_list in cookie_list
    push!(total_calories, sum(sub_list))  # Calculate the total and store it
end

# Sort the totals in descending order and take the top 3
largest_3 = sort(total_calories, rev=true)[1:3]
println("Part 2:", sum(largest_3))