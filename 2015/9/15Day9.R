# Load necessary library
library(stringr)

# Define the file name and path
D9_file <- 'Day9_routes.txt'
D9_file_path <- file.path(dirname(rstudioapi::getActiveDocumentContext()$path), D9_file)

# Read the file
routes_list <- readLines(D9_file_path)

# Print the routes list
print(routes_list[2])
