# Advent of Code - Day 13, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/13
# Solution by: [abbasmoosajee07]
# Brief: [Seating Problem]

required_packages <- c("ggplot2", "dplyr", "tidyr", "igraph", "stringr", "gtools")

# Check and install missing packages
for (package in required_packages) {
  if (!requireNamespace(package, quietly = TRUE)) {
    install.packages(package)
  }
  library(package, character.only = TRUE)
}


# Define the file name and path
d13_file <- "Day13_input.txt"
d13_file_path <- file.path(dirname(rstudioapi::getActiveDocumentContext()$path),
                           d13_file)

input_data <- readLines(d13_file_path)



# Function to calculate happiness for seating arrangements
happy_seating <- function(seating_matrix, starting_person, number_of_people) {
  # Get the set of guests apart from the starting person
  vertex <- setdiff(1:number_of_people, starting_person)
  # Get all permutations of seating arrangements
  total_permutations <- permutations(length(vertex), length(vertex), vertex) # nolint: object_usage_linter.
  max_happiness <- 0
  
  # Iterate over all permutations and calculate happiness
  for (permutation in 1:nrow(total_permutations)) { # nolint: seq_linter.
    current_happiness <- 0
    outer_array_index <- starting_person
    
    for (inner_index in total_permutations[permutation, ]) {
      current_happiness <- current_happiness +
        seating_matrix[outer_array_index, inner_index] +
        seating_matrix[inner_index, outer_array_index]
      outer_array_index <- inner_index
    }
    
    # Close the loop by returning to the starting person
    current_happiness <- current_happiness +
      seating_matrix[outer_array_index, starting_person] +
      seating_matrix[starting_person, outer_array_index]
    
    # Track maximum happiness
    max_happiness <- max(max_happiness, current_happiness)
  }
  
  return(max_happiness)
}

# Function to create dictionary from input sentences
create_dictionary <- function(sentences) {
  seating_dictionary <- list()
  
  for (sentence in sentences) {
    matches <- regmatches(sentence, regexec("(\\w+) would (gain|lose) (\\d+) happiness units by sitting next to (\\w+).", sentence))
    person <- matches[[1]][2]
    gain_or_lose <- matches[[1]][3]
    number <- as.integer(matches[[1]][4])
    neighbor <- matches[[1]][5]

    if (gain_or_lose == "lose") {
      number <- -number
    }
    
    if (!is.list(seating_dictionary[[person]])) {
      seating_dictionary[[person]] <- list()
    }
    
    seating_dictionary[[person]][[neighbor]] <- number
  }
  
  return(seating_dictionary)
}

# Function to create adjacency matrix from dictionary
create_graph <- function(input_dictionary) {
  people <- names(input_dictionary)
  matrix_size <- length(people)
  matrix <- matrix(0, nrow = matrix_size, ncol = matrix_size)

  for (i in 1:matrix_size) {
    for (j in 1:matrix_size) {
      if (i != j) {
        person1 <- people[i]
        person2 <- people[j]
        matrix[i, j] <- input_dictionary[[person1]][[person2]]
      }
    }
  }
  
  return(matrix)
}

# Add myself to the combination of guest----------------------------------------
add_guest <- function(list, new_name, happiness) {
  guest_dictionary <- create_dictionary(list)
  unique_names <- unique(c(names(guest_dictionary), unlist(lapply(guest_dictionary, names))))

  extra_combos <- c()
  for (name in unique_names){
    combo_1 <- paste0(new_name, " would gain ", happiness,
                   " happiness units by sitting next to ", name, ".")
    combo_2 <- paste0(name, " would gain ", happiness,
                      " happiness units by sitting next to ", new_name, ".")
    extra_combos <- c(extra_combos, combo_1, combo_2)
  }
  
  new_list <- c(list, extra_combos)
  return(new_list)
}

new_list <- add_guest(input_data,"Abbas", 0)

# Main execution----------------------------------------------------------------
guest_dictionary <- create_dictionary(input_data)
guest_matrix <- create_graph(guest_dictionary)
final_happiness_level <- happy_seating(guest_matrix, 1, nrow(guest_matrix))
cat("The greatest happiness level with the best seating arrangement is", final_happiness_level, "\n")


guest_dictionary_new <- create_dictionary(new_list)
guest_matrix_new <- create_graph(guest_dictionary_new)
new_happiness_level <- happy_seating(guest_matrix_new, 1, nrow(guest_matrix_new))
cat("The greatest happiness level including you is", new_happiness_level, "\n")
