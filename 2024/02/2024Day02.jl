#=
Advent of Code - Day 2, Year 2024
Solution Started: Dec 2, 2024
Puzzle Link: https://adventofcode.com/2024/day/2
Solution by: abbasmoosajee07
Brief: [Validate Reports]
=#

#!/usr/bin/env julia

using Printf, DelimitedFiles

# Define constant for the input file
const D02_FILE = "Day02_input.txt"
const D02_FILE_PATH = joinpath(dirname(@__FILE__), D02_FILE)
input_data = readlines(D02_FILE_PATH)

# Function to check if the report is valid based on the rules
function check_validity(report::Vector{Int})
    # Calculate the differences between consecutive elements
    diffs = report[2:end] .- report[1:end-1]

    # Check if the differences are all either increasing or decreasing
    if (all(sign.(diffs) .== 1) || all(sign.(diffs) .== -1))
            # Check if the absolute values of the differences are within the valid range (1 to 3)
        if all(1 .<= abs.(diffs) .<= 3)
            return true
        end
        return false
    end
    return false
end

function compute(input_data, tolerance = 0)
    valid_reports = 0
    
    for line in input_data
        # Parse the line into integers
        report = parse.(Int, split(line))

        # Check if the report is valid, or if it becomes valid by removing one element
        if check_validity(report) || any(check_validity(vcat(report[1:i-tolerance],
                                report[i+tolerance:end])) for i in eachindex(report))
            valid_reports += 1
        end
    end
    
    return valid_reports
end


# Call the compute function with the input file path
ans_p1 = compute(input_data)
println("Part 1: ", ans_p1)

ans_p2 = compute(input_data, 1)
println("Part 2: ", ans_p2)