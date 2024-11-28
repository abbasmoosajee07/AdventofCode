# Advent of Code - Day 2, Year 2022
# Solution Started: Nov 27, 2024
# Puzzle Link: https://adventofcode.com/2022/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Rock, Papers and Scissors]

#!/usr/bin/env julia

using Printf, DelimitedFiles

# Load the input data from the specified file path
const D02_FILE = "Day02_input.txt"
const D02_FILE_PATH = joinpath(dirname(@__FILE__), D02_FILE)

# Read the input data
input_data = readlines(D02_FILE_PATH)

function play_rock_paper_scissors(round)
    # Move mappings (A, B, C -> X, Y, Z)
    move_map = Dict("A" => "X", "B" => "Y", "C" => "Z")
    score_map = Dict("X" => 1, "Y" => 2, "Z" => 3)

    # Translate opponent's and your moves
    opponent_move = move_map[round[1]]
    your_move = round[2]

    # Determine the result: 0 = loss, 3 = draw, 6 = win
    if your_move == opponent_move
        result_score = 3   # Draw
    elseif  (your_move == "X" && opponent_move == "Z") ||  # You play Rock, other plays Scissors (Win)
            (your_move == "Y" && opponent_move == "X") ||  # You play Paper, other plays Rock (Win)
            (your_move == "Z" && opponent_move == "Y")     # You play Scissors, other plays Paper (Win)
        result_score = 6   # Win
    else
        result_score = 0   # Loss
    end

    # Total score: Hand score + result score
    return score_map[your_move] + result_score
end

function select_rock_paper_scissors(round)
    # Move mappings (A, B, C -> X, Y, Z)
    move_map = Dict("A" => "X", "B" => "Y", "C" => "Z")
    score_map = Dict("X" => 1, "Y" => 2, "Z" => 3)

    # Translate opponent's and desired result moves
    opponent_move = move_map[round[1]]
    desired_result = round[2]

    # Initialize your_move and result_score
    if desired_result == "X"
        result_score = 0  # You want to lose
        if opponent_move == "X"
            your_move = "Z"  # Rock loses to Scissors
        elseif opponent_move == "Y"
            your_move = "X"  # Paper loses to Rock
        elseif opponent_move == "Z"
            your_move = "Y"  # Scissors loses to Paper
        end
    elseif desired_result == "Y"
        result_score = 3  # Draw
        your_move = opponent_move  # Draw: same move as opponent
    elseif desired_result == "Z"
        result_score = 6  # Win
        if opponent_move == "X"
            your_move = "Y"  # Rock beats Scissors
        elseif opponent_move == "Y"
            your_move = "Z"  # Paper beats Rock
        elseif opponent_move == "Z"
            your_move = "X"  # Scissors beats Paper
        end
    end

    # Total score: Hand score + result score
    return result_score + score_map[your_move]
end

total_score_p1 = 0
total_score_p2 = 0

for hands in input_data
    round = split(hands, " ")
    score_p1 = play_rock_paper_scissors(round)
    score_p2 = select_rock_paper_scissors(round)
    global total_score_p1 += score_p1
    global total_score_p2 += score_p2
end

println("Part 1: ", total_score_p1)
println("Part 2: ", total_score_p2)



