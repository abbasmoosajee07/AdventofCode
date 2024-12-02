=begin
Advent of Code - Day 11, Year 2022
Solution Started: Dec 1, 2024
Puzzle Link: https://adventofcode.com/2022/day/11
Solution by: abbasmoosajee07
Brief: [Monkey and Worry Lists]
=end

#!/usr/bin/env ruby

require 'pathname'
require 'set'

# Define file name and extract complete path to the input file
D11_file = "Day11_input.txt"
D11_file_path = Pathname.new(__FILE__).dirname + D11_file

input_data = File.read(D11_file_path).strip.split("\n\n")

def parse_input(monkey_list)
  """Parses input and returns a hash representing each monkey's data."""
  monkey_dict = {}
  
  monkey_list.each do |monkey|
    monkey_data = monkey.split("\n")
    monkey_no = monkey_data[0].gsub('Monkey ', '').gsub(':', '').to_i
    starting = monkey_data[1].gsub('Starting items: ', '').split(',').map(&:to_i)
    operation = monkey_data[2].split(' = ')[1]
    test = monkey_data[3].gsub('Test: divisible by ', '').to_i
    true_throw = monkey_data[4].gsub('If true: throw to monkey ', '').to_i
    false_throw = monkey_data[5].gsub('If false: throw to monkey ', '').to_i
    
    monkey_dict[monkey_no] = {
      starting: starting,
      op: operation,
      test: test,
      true_throw: true_throw,
      false_throw: false_throw,
      inspect: 0
    }
  end
  
  monkey_dict
end

def basic_monkey_turn(monkey_dict, no, modulus = None)
  """Performs a single turn for the given monkey."""
  monkey_data = monkey_dict[no]
  worry_list = monkey_data[:starting]
  operation = monkey_data[:op]
  
  worry_list.each do |worry_level|
    old = worry_level
    
    # Substitute 'old' into the operation and evaluate
    expr = operation.gsub('old', old.to_s)
    result = eval(expr)
    
    # Calculate new worry level and decide which monkey to throw to
    new_worry = result / 3
    throw = (new_worry % monkey_data[:test]).zero? ? monkey_data[:true_throw] : monkey_data[:false_throw]
    
    # Add new worry level to the target monkey's starting list
    monkey_dict[throw][:starting] << new_worry
    
    # Increment the inspection counter
    monkey_dict[no][:inspect] += 1
  end
  
  # Clear the current monkey's 'starting' list
  monkey_data[:starting] = []
end

def busiest_monkeys(monkey_dict)
  """Calculates the product of the two highest inspection counts."""
  inspect_counts = monkey_dict.values.map { |data| data[:inspect] }
  sorted_counts = inspect_counts.sort.reverse
  sorted_counts[0] * sorted_counts[1]
end

def lcm(a, b)
  """Calculate the Least Common Multiple (LCM) of two numbers."""
  a.lcm(b)
end

def compute_lcm_of_tests(monkey_dict)
  """Compute the LCM of all test divisors."""
  test_values = monkey_dict.values.map { |data| data[:test] }
  test_values.reduce { |acc, val| lcm(acc, val) }
end

def modular_monkey_turn(monkey_dict, no, modulus)
  """Perform a single turn for the given monkey, using modular arithmetic."""
  monkey_data = monkey_dict[no]
  worry_list = monkey_data[:starting]
  operation = monkey_data[:op]
  
  worry_list.each do |worry_level|
    old = worry_level
    
    # Substitute 'old' into the operation and evaluate
    expr = operation.gsub('old', old.to_s)
    result = eval(expr)
    
    # Apply modular arithmetic to limit worry level growth
    new_worry = result % modulus
    
    # Determine which monkey to throw to based on divisibility test
    throw = (new_worry % monkey_data[:test]).zero? ? monkey_data[:true_throw] : monkey_data[:false_throw]
    
    # Add the new worry level to the target monkey's starting list
    monkey_dict[throw][:starting] << new_worry
    
    # Increment the inspection counter
    monkey_dict[no][:inspect] += 1
  end
  
  # Clear the current monkey's 'starting' list
  monkey_data[:starting] = []
end

def play_rounds(monkey_dict, turn_function, total_rounds, modulus = nil)
  """Simulates multiple rounds of monkey operations."""
  total_rounds.times do |_|
    monkey_dict.keys.sort.each do |key| # Ensure deterministic order
      turn_function.call(monkey_dict, key, modulus)
    end
  end
  busy_score = busiest_monkeys(monkey_dict)
  [monkey_dict, busy_score]
end

# Part 1: Basic Simulation
monkey_dict = parse_input(input_data)
final_dict_p1, ans_p1 = play_rounds(monkey_dict.dup, method(:basic_monkey_turn), 20)
puts "Part 1: #{ans_p1}"

# Part 2: Modular Arithmetic Simulation
monkey_dict = parse_input(input_data)
modulus = compute_lcm_of_tests(monkey_dict)
final_dict_p2, ans_p2 = play_rounds(monkey_dict, method(:modular_monkey_turn), 10_000, modulus)
puts "Part 2: #{ans_p2}"

