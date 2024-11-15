# Advent of Code - Day 25, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/25
# Solution by: [abbasmoosajee07]
# Brief: [Reading instructions]
require 'set'
require 'pathname'

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = Pathname.new(__FILE__).dirname.join(D25_file)

def parse_input(text)
  init_state = text.match(/Begin in state (.)\./)[1]
  steps = text.match(/after (\d+) steps/)[1].to_i
  rules = {}
  dirs = { 'right' => 1, 'left' => -1 }
  
  # Use regex to capture the rules
  text.scan(/In state (.)/).each do |state|
    state = state[0]
    # Match actions for current state
    if text =~ /In state #{state}:\s*If the current value is 0:\s*- Write the value (.)\.\s*- Move one slot to the (\w+)\.\s*- Continue with state (.)\.\s*If the current value is 1:\s*- Write the value (.)\.\s*- Move one slot to the (\w+)\.\s*- Continue with state (.)/
      rules[state] = [
        { write: $1.to_i, move: dirs[$2], state: $3 },
        { write: $4.to_i, move: dirs[$5], state: $6 }
      ]
    end
  end

  [init_state, steps, rules]
end

def run(blueprint)
  state, steps, rules = parse_input(blueprint)
  tape = Hash.new(0)  # Default value of 0 for each key
  cursor = 0

  steps.times do
    action = rules[state][tape[cursor]]
    tape[cursor] = action[:write]
    cursor += action[:move]
    state = action[:state]
  end

  # Count number of 1s in the tape
  tape.count { |_, v| v == 1 }
end

if __FILE__ == $0
  input_data = File.read(D25_file_path)
  puts "Part 1: #{run(input_data)}"
end
