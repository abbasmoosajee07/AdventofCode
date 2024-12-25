=begin
Advent of Code - Day 6, Year 2023
Solution Started: Dec 25, 2024
Puzzle Link: https://adventofcode.com/2023/day/6
Solution by: abbasmoosajee07
Brief: [Winning a boat race]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D06_file = "Day06_input.txt"
D06_file_path = Pathname.new(__FILE__).dirname + D06_file

# Read the input data
input_data = File.readlines(D06_file_path).map(&:strip)

def parse_input(race_info)
  race_dict = {}
  time_list = race_info[0].scan(/\d+/).map(&:to_i)
  distance_list = race_info[1].scan(/\d+/).map(&:to_i)

  time_list.each_with_index do |time, index|
    race_dict[time] = distance_list[index]
  end

  full_time = time_list.join.to_i
  full_distance = distance_list.join.to_i
  full_race = [full_time, full_distance]

  [race_dict, full_race]
end

def win_race(time, distance)
  total_wins = 0

  (0...time).each do |press_button|
    speed = press_button * 1
    final_distance = (time - press_button) * speed

    total_wins += 1 if final_distance > distance
    # Uncomment the following line for debugging:
    # puts "press_button=#{press_button}, speed=#{speed}, final_distance=#{final_distance}, total_wins=#{total_wins}"
  end

  total_wins
end

# Test input
test_input = ['Time:      7  15   30', 'Distance:  9  40  200']
races, long_race = parse_input(input_data)

all_wins = []
races.each do |time, distance|
  race_win = win_race(time, distance)
  all_wins << race_win if race_win != 0
end

part1_result = all_wins.reduce(1, :*) # Product of all wins
puts "Part 1: #{part1_result}"

big_race_wins = win_race(long_race[0], long_race[1])
puts "Part 2: #{big_race_wins}"
