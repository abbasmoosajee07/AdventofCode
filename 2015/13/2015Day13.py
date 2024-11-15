# Advent of Code - Day 13, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/13
# Solution by: [abbasmoosajee07]
# Brief: [Seating Problem]

import itertools, os, re

# Function to calculate happiness for seating arrangements
def happy_seating(seating_matrix, starting_person, number_of_people):
    # Get the set of guests apart from the starting person
    vertex = [i for i in range(number_of_people) if i != starting_person]
    total_permutations = itertools.permutations(vertex)
    max_happiness = 0
    
    # Iterate over all permutations and calculate happiness
    for permutation in total_permutations:
        current_happiness = 0
        outer_array_index = starting_person
        
        for inner_index in permutation:
            current_happiness += seating_matrix[outer_array_index][inner_index] + seating_matrix[inner_index][outer_array_index]
            outer_array_index = inner_index
        
        # Close the loop by returning to the starting person
        current_happiness += seating_matrix[outer_array_index][starting_person] + seating_matrix[starting_person][outer_array_index]
        
        # Track maximum happiness
        max_happiness = max(max_happiness, current_happiness)
    
    return max_happiness

# Function to create dictionary from input sentences
def create_dictionary(sentences):
    seating_dictionary = {}
    
    for sentence in sentences:
        # Regex matching pattern for the input
        match = re.match(r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).", sentence)
        if match:
            person = match[1]
            gain_or_lose = match[2]
            number = int(match[3])
            neighbor = match[4]
            
            if gain_or_lose == "lose":
                number = -number
            
            if person not in seating_dictionary:
                seating_dictionary[person] = {}
            seating_dictionary[person][neighbor] = number
    
    return seating_dictionary

# Function to create adjacency matrix from dictionary
def create_graph(input_dictionary):
    people = list(input_dictionary.keys())
    matrix_size = len(people)
    matrix = [[0] * matrix_size for _ in range(matrix_size)]
    
    for i in range(matrix_size):
        for j in range(matrix_size):
            if i != j:
                person1 = people[i]
                person2 = people[j]
                matrix[i][j] = input_dictionary[person1].get(person2, 0)
    
    return matrix

# Add myself to the combination of guest
def add_guest(guest_list, new_name, happiness):
    guest_dictionary = create_dictionary(guest_list)
    unique_names = list(set(guest_dictionary.keys()).union({name for sublist in guest_dictionary.values() for name in sublist}))
    
    extra_combos = []
    for name in unique_names:
        combo_1 = f"{new_name} would gain {happiness} happiness units by sitting next to {name}."
        combo_2 = f"{name} would gain {happiness} happiness units by sitting next to {new_name}."
        extra_combos.extend([combo_1, combo_2])
    
    new_list = guest_list + extra_combos
    return new_list

# Main execution
if __name__ == "__main__":
    # Read the input file
    D13_file = 'Day13_input.txt'
    D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)

    with open(D13_file_path, 'r') as file:
        input_data = file.readlines()
    
    # First round without the new guest
    guest_dictionary = create_dictionary(input_data)
    guest_matrix = create_graph(guest_dictionary)
    final_happiness_level = happy_seating(guest_matrix, 0, len(guest_matrix))
    print(f"The greatest happiness level with the best seating arrangement is {final_happiness_level}")
    
    # Add new guest "Abbas" with happiness 0
    new_list = add_guest(input_data, "Abbas", 0)
    
    # Second round with the new guest
    guest_dictionary_new = create_dictionary(new_list)
    guest_matrix_new = create_graph(guest_dictionary_new)
    new_happiness_level = happy_seating(guest_matrix_new, 0, len(guest_matrix_new))
    print(f"The greatest happiness level including you is {new_happiness_level}")
