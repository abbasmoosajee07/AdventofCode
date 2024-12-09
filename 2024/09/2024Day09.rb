=begin
Advent of Code - Day 9, Year 2024
Solution Started: Dec 9, 2024
Puzzle Link: https://adventofcode.com/2024/day/9
Solution by: abbasmoosajee07
Brief: [Free up Disk Space]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D09_file = "Day09_input.txt"
D09_file_path = Pathname.new(__FILE__).dirname + D09_file

# Read and sort input data into a grid
input_data = File.read(D09_file_path).strip.split("\n")[0]

def calculate_checksum(file)
  checksum = 0
  file.each_with_index do |num, pos|
    checksum += pos * num.to_i
  end
  checksum
end

def create_file(file_str)
  id = 0
  expanded_file = []
  file_list = file_str.chars
  file_list.each_with_index do |space, pos|
    space = space.to_i
    if pos.even?
      add_file = [id.to_s] * space
      id += 1
    else
      add_file = ['.'] * space
    end
    expanded_file.append(add_file)
  end
  expanded_file
end

def free_disk_space(file_list)
  flat_file = file_list.flatten

  defragmented_file = flat_file.clone
  empty_spaces = flat_file.each_index.select { |index| flat_file[index] == '.' }
  full_file = flat_file.reject { |value| value == '.' }

  empty_spaces.each do |pos|
    type = defragmented_file[pos]
    last_pos = full_file.last
    defragmented_file[pos] = last_pos
    full_file.pop
  end
  defragmented_file = defragmented_file[0...-empty_spaces.length]
  calculate_checksum(defragmented_file)
end

def reorganize_files(disk_code)
  d = {}
  frees = []
  counter = 0

  # Create the file representation from disk code
  disk_code.each_with_index do |r, i|
    start, finish = counter, counter + r
    if i.even?
      d[i / 2] = [start, finish]
    elsif r > 0
      frees.append([start, finish])
    end
    counter += r
  end

  # Two pointers to track the files and the free gaps
  idx_ptr = d.keys.max

  while idx_ptr >= 0
    file_start, file_end = d[idx_ptr]
    file_len = file_end - file_start

    free_ptr = 0
    while free_ptr < frees.length
      gap_start, gap_end = frees[free_ptr]
      if gap_start >= file_start
        break
      end

      gap_len = gap_end - gap_start
      if file_len <= gap_len
        frees.delete_at(free_ptr)

        # Move file to the gap
        new_file_start, new_file_end = gap_start, gap_start + file_len
        new_gap_start, new_gap_end = new_file_end, gap_end

        # Update file and gap positions
        d[idx_ptr] = [new_file_start, new_file_end]
        frees.insert(free_ptr, [new_gap_start, new_gap_end]) if new_gap_start != new_gap_end
        break
      else
        free_ptr += 1
      end
    end

    idx_ptr -= 1
  end

  # Calculate the result
  result = 0
  d.each do |k, (start, finish)|
    result += (start...finish).sum { |i| k * i }
  end
  [result, d]
end

file_p1 = input_data
fragmented_file = create_file(file_p1)
ans_p1 = free_disk_space(fragmented_file)
puts "Part 1: #{ans_p1}"

file_p2 = input_data.chars.join.split('').map(&:to_i)
# Reorganize and calculate the checksum for part 2
ans_p2, file = reorganize_files(file_p2)
puts "Part 2: #{ans_p2}"
