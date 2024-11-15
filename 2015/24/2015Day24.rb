# Advent of Code - Day 24, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/24
# Solution by: [abbasmoosajee07]
# Brief: [Variation of the Container Problem]

require 'pathname'

# Define the file path
D24_file = 'Day24_input.txt'
D24_file_path = Pathname.new(__FILE__).dirname + D24_file

# Read the contents of the file
packages_input = File.readlines(D24_file_path).map(&:chomp)

def create_package_combo(packages, group_no)
  packages = packages.map{|x| x.to_i}
  package_combinations = (1..packages.length).map{|x| packages.combination(x).map{|y| y if y.sum == packages.sum/group_no}.compact}
                                            .compact
                                            .reject(&:empty?)
                                            .flatten(1)
  santa_leg_room_packages = 100000000000000000
  package_combinations.each {|combination| santa_leg_room_packages = [santa_leg_room_packages, combination.length].min}
  group_1_contenders = package_combinations.map {|combination| combination if combination.length == santa_leg_room_packages}
                                          .compact
  if group_1_contenders.length == 1
    puts "The quantum entanglement of the packages in Santa's leg area is #{group_1_contenders[0].reduce(1){|prod, num| prod * num}}"
  else
    quantum_entanglement = 10000000000000000000000
    group_1_contenders.each{|contender| quantum_entanglement = [quantum_entanglement, contender.reduce(1){|prod, num| prod * num}].min}
    puts "The quantum entanglement of the packages organised in #{group_no} groups, is #{quantum_entanglement}}"
  end
end

Part_1 = create_package_combo(packages_input, 3)

Part_2 = create_package_combo(packages_input, 4)