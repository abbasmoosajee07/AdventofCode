require 'matrix'

D6_file = 'Day6_lights.txt'
D6_file_path = File.join(File.dirname(File.expand_path(__FILE__)), D6_file)

lights_inst = File.read(D6_file_path).split("\n")

def parse_instruction(instruction)
  # Regex to capture the action and the four numbers (coordinates)
  match = instruction.match(/(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)/)

  if match
    action = match[1]
    x1 = match[2].to_i
    y1 = match[3].to_i
    x2 = match[4].to_i
    y2 = match[5].to_i

    # Return in the required format
    [action, x1, y1, x2, y2]
  else
    nil
  end
end

instruction_matrix = []

lights_inst.each do |instruction_n|
  instruction_matrix << parse_instruction(instruction_n)
end

# Create a 1000x1000 matrix for light status
light_matrix_1 = Array.new(1000) { Array.new(1000, 0) }

instruction_matrix.each do |instruction_n|
  action = instruction_n[0]
  x1 = instruction_n[1]
  y1 = instruction_n[2]
  x2 = instruction_n[3]
  y2 = instruction_n[4]

  (x1..x2).each do |x|
    (y1..y2).each do |y|
      case action
      when "turn on"
        light_matrix_1[x][y] = 1
      when "turn off"
        light_matrix_1[x][y] = 0
      when "toggle"
        light_matrix_1[x][y] = 1 - light_matrix_1[x][y] # Toggle the light
      end
    end
  end
end

total_sum_1 = light_matrix_1.flatten.sum
puts "Total houses with lights on: #{total_sum_1}"

# Create a 1000x1000 matrix for brightness
light_matrix_2 = Array.new(1000) { Array.new(1000, 0) }

instruction_matrix.each do |instruction_n|
  action = instruction_n[0]
  x1 = instruction_n[1]
  y1 = instruction_n[2]
  x2 = instruction_n[3]
  y2 = instruction_n[4]

  (x1..x2).each do |x|
    (y1..y2).each do |y|
      case action
      when "turn on"
        light_matrix_2[x][y] += 1
      when "turn off"
        light_matrix_2[x][y] -= 1
        light_matrix_2[x][y] = 0 if light_matrix_2[x][y] < 0
      when "toggle"
        light_matrix_2[x][y] += 2
      end
    end
  end
end

total_sum_2 = light_matrix_2.flatten.sum
puts "Total brightness of houses: #{total_sum_2}"
