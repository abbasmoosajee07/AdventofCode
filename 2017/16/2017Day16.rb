# Advent of Code - Day 16, Year 2017
# Solved in: 2024
# https://adventofcode.com/2017/day/16
# Solution by: [abbasmoosajee07]
# Brief: [String Scrambler]

require 'pathname'

# Load the input data from the specified file path
D16_file = "Day16_input.txt"

# Define the file path
D16_file_path = Pathname.new(__FILE__).dirname + D16_file
input_data = File.read(D16_file_path).strip.split(',')
letters_list = ('a'..'p').to_a

class Scrambler
  attr_accessor :string

  def initialize(string)
    @string = string
  end

  def spin(x)
    x = x % @string.length
    @string = @string[-x..-1] + @string[0...-x]
  end

  def exchange(a, b)
    str_arr = @string.chars
    str_arr[a], str_arr[b] = str_arr[b], str_arr[a]
    @string = str_arr.join
  end

  def partner(a, b)
    a_index = @string.index(a)
    b_index = @string.index(b)
    exchange(a_index, b_index) if a_index && b_index
  end

  def execute(command)
    case command[0]
    when 'spin'
      spin(command[1].to_i)
    when 'exchange'
      exchange(command[1].to_i, command[2].to_i)
    when 'partner'
      partner(command[1], command[2])
    end
  end
end

def parse_instruction(instruction)
  parsed_commands = []

  if instruction =~ /^s(\d+)/
    x = $1.to_i
    parsed_commands << ['spin', x]
  elsif instruction =~ /^x(\d+)\/(\d+)/
    a, b = $1.to_i, $2.to_i
    parsed_commands << ['exchange', a, b]
  elsif instruction =~ /^p(\w+)\/(\w+)/
    a, b = $1, $2
    parsed_commands << ['partner', a, b]
  end

  parsed_commands
end

def create_command_list(instruction_list)
  instruction_list.flat_map { |instruction| parse_instruction(instruction) }
end

def scramble(initial_string, input_data)
  scrambler = Scrambler.new(initial_string)
  command_list = create_command_list(input_data)

  command_list.each { |command| scrambler.execute(command) }

  scrambler.string
end

def find_cycle(initial_string, input_data)
  seen_states = {}
  input_string = initial_string
  iteration = 0

  loop do
    if seen_states.key?(input_string)
      cycle_length = iteration - seen_states[input_string]
      remaining_iterations = (1_000_000_000 - iteration) % cycle_length
      remaining_iterations.times do
        input_string = scramble(input_string, input_data)
      end
      break
    end
    seen_states[input_string] = iteration
    input_string = scramble(input_string, input_data)
    iteration += 1
  end

  input_string
end

initial_string = "abcdefghijklmnop"
puts "Part 1:"
puts "Initial: #{initial_string}"

# Scramble once for Part 1
scrambled_once = scramble(initial_string, input_data)
puts "Scrambled after 1 iteration: #{scrambled_once}"

# Part 2: Find the final state after 1 billion iterations
final_string = find_cycle(initial_string, input_data)
puts "Final after 1 billion iterations: #{final_string}"

