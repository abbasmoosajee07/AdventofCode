#=
Advent of Code - Day 5, Year 2024
Solution Started: Dec 5, 2024
Puzzle Link: https://adventofcode.com/2024/day/5
Solution by: abbasmoosajee07
Brief: [Validating Reports]
=#

#!/usr/bin/env julia

# Load the input data from the specified file path
const D05_FILE = "Day05_input.txt"
const D05_FILE_PATH = joinpath(dirname(@__FILE__), D05_FILE)

# Read and split the input data into sections
input_data = split(strip(read(D05_FILE_PATH, String)), "\n\n")

# Function to apply rules to the given book list
function apply_rule(book, rules)
    # Check if any rule applies; return 0 if true, otherwise return the middle element of the book list
    for rule in rules
        if in(rule[1], book) && in(rule[2], book) && findfirst(isequal(rule[1]), book) > findfirst(isequal(rule[2]), book)
            return 0
        end
    end
    return book[div(length(book), 2) + 1]
end

# Function to swap elements in the book list based on rules
function swap_elements(book, rules)
    for rule in rules
        if in(rule[1], book) && in(rule[2], book) && findfirst(isequal(rule[1]), book) > findfirst(isequal(rule[2]), book)
            # Swap the elements in the book list
            index_0, index_1 = findfirst(isequal(rule[1]), book), findfirst(isequal(rule[2]), book)
            book[index_0], book[index_1] = book[index_1], book[index_0]
            return true
        end
    end
    return false
end

# Main function to calculate the results for Part 1 and Part 2
function calculate_results(rules, update_list)
    mid_p1 = 0
    mid_p2 = 0

    for book in update_list
        res = apply_rule(book, rules)
        mid_p1 += res

        # For Part 2, apply the rule multiple times if the result is 0
        if res == 0
            while swap_elements(book, rules)
                mid_p2 += apply_rule(book, rules)
            end
        end
    end

    return mid_p1, mid_p2
end

# Convert the input data to the appropriate format
manual_dict = [parse.(Int, split(line, "|")) for line in split(input_data[1], "\n")]
update_list = [parse.(Int, split(line, ",")) for line in split(input_data[2], "\n")]

# Calculate and print the results for both parts
ans_p1, ans_p2 = calculate_results(manual_dict, update_list)
println("Part 1: ", ans_p1)
println("Part 2: ", ans_p2)

