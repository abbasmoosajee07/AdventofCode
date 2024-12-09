=begin
Advent of Code - Day 19, Year 2022
Solution Started: Dec 9, 2024
Puzzle Link: https://adventofcode.com/2022/day/19
Solution by: abbasmoosajee07
Brief: [Mining Robots]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D19_file = "Day19_input.txt"
D19_file_path = Pathname.new(__FILE__).dirname + D19_file

# Read the input data
input_data = File.read(D19_file_path)

def parse_input(input)
  input.split("\n").map do |line|
    line.scan(/\d+/).map(&:to_i)
  end
end

def solve(time_left, build_costs, material_inventory, robot_inventory, max_geode, allow)
  can_build = [
    material_inventory[0] >= build_costs[0],
    material_inventory[0] >= build_costs[1],
    material_inventory[0] >= build_costs[2] && material_inventory[1] >= build_costs[3],
    material_inventory[0] >= build_costs[4] && material_inventory[2] >= build_costs[5]
  ]

  return material_inventory[3] if time_left == 0

  new_materials = material_inventory.zip(robot_inventory).map { |m, r| m + r }

  # Pruning:
  max_additional_geode = if can_build[3]
                           time_left * robot_inventory[3] + time_left * (time_left - 1) / 2
                         else
                           time_left * robot_inventory[3] + (time_left - 1) * (time_left - 2) / 2
                         end

  return max_geode if material_inventory[3] + max_additional_geode <= max_geode

  if can_build[3]
    geode = solve(time_left - 1, build_costs,
                  new_materials.zip([build_costs[4], 0, build_costs[5], 0]).map { |a, b| a - b },
                  robot_inventory.zip([0, 0, 0, 1]).map { |a, b| a + b },
                  max_geode, [true, true, true, true])
    max_geode = [max_geode, geode].max
    return max_geode
  end

  if can_build[2] && allow[2] && build_costs[5] >= robot_inventory[2]
    geode = solve(time_left - 1, build_costs,
                  new_materials.zip([build_costs[2], build_costs[3], 0, 0]).map { |a, b| a - b },
                  robot_inventory.zip([0, 0, 1, 0]).map { |a, b| a + b },
                  max_geode, [true, true, true, true])
    max_geode = [max_geode, geode].max
  end

  if can_build[1] && allow[1] && build_costs[3] >= robot_inventory[1]
    geode = solve(time_left - 1, build_costs,
                  new_materials.zip([build_costs[1], 0, 0, 0]).map { |a, b| a - b },
                  robot_inventory.zip([0, 1, 0, 0]).map { |a, b| a + b },
                  max_geode, [true, true, true, true])
    max_geode = [max_geode, geode].max
  end

  if can_build[0] && allow[0] && [build_costs[0], build_costs[1], build_costs[2], build_costs[4]].max >= robot_inventory[0]
    geode = solve(time_left - 1, build_costs,
                  new_materials.zip([build_costs[0], 0, 0, 0]).map { |a, b| a - b },
                  robot_inventory.zip([1, 0, 0, 0]).map { |a, b| a + b },
                  max_geode, [true, true, true, true])
    max_geode = [max_geode, geode].max
  end

  if !can_build[3]
    geode = solve(time_left - 1, build_costs, new_materials, robot_inventory, max_geode, can_build.map { |x| !x })
    max_geode = [max_geode, geode].max
  end

  max_geode
end


blueprints = parse_input(input_data)

p1tasks = []
blueprints.each do |blueprint|
  p1tasks << Thread.new do
    blueprint[0] * solve(24, blueprint[1..-1], [0, 0, 0, 0], [1, 0, 0, 0], 0, [true, true, true, true])
  end
end

p2tasks = []
blueprints[0, [blueprints.length, 3].min].each do |blueprint|
  p2tasks << Thread.new do
    solve(32, blueprint[1..-1], [0, 0, 0, 0], [1, 0, 0, 0], 0, [true, true, true, true])
  end
end

p1 = p1tasks.map(&:value).sum
p2 = p2tasks.map(&:value).reduce(:*)
puts "Part 1: #{p1}"
puts "Part 2: #{p2}"
