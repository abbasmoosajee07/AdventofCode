# Advent of Code - Day 9, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/9
# Solution by: [abbasmoosajee07]
# Brief: [Standard Travelling Salesman Problem]

# List of required packages
required_packages <- c("ggplot2", "dplyr", "tidyr", "gtools", "stringr", "rstudioapi")

# Check and install missing packages
for (package in required_packages) {
  if (!requireNamespace(package, quietly = TRUE)) {
    install.packages(package)
  }
  library(package, character.only = TRUE)
}


# Define the file name and path
d9_file <- "Day09_input.txt"
d9_file_path <- file.path(dirname(rstudioapi::getActiveDocumentContext()$path),d9_file) # no lint

# Function to parse a line of input
parse_line <- function(line) {
  words <- unlist(strsplit(trimws(line), " "))
  return(c(words[1], words[3], as.numeric(words[length(words)])))
}

# Lookup function for distance
lookup_dist <- function(start, end, dist) {
  stopifnot(start %in% names(dist), end %in% names(dist))
  if (start == end) {
    return(0)
  }
  if (!is.null(dist[[start]][[end]])) {
    return(dist[[start]][[end]])
  }
  return(10000) # Large number for unconnected cities
}

# Function to calculate all possible routes and their distances
calculate_routes <- function(graph) {
  cities <- names(graph)[names(graph) != "dummy"]
  all_routes <- permutations(n = length(cities), r = length(cities), v = cities) # nolint

  route_distances <- data.frame(route = character(),
                                distance = numeric(), stringsAsFactors = FALSE)

  for (i in 1:nrow(all_routes)) { # nolint: seq_linter.
    route <- all_routes[i, ]
    distance <- 0
    for (j in 1:(length(route) - 1)) {
      distance <- distance + lookup_dist(route[j], route[j + 1], graph)
    }
    route_distances <- rbind(route_distances,
                             data.frame(route = paste(route, collapse = " -> "),
                                        distance = distance))
  }

  return(route_distances)
}

# Main function to read the input and build the graph
graph <- list()
input <- readLines(d9_file_path)

for (line in input) {
  parsed <- parse_line(line)
  start <- parsed[1]
  end <- parsed[2]
  dist <- as.numeric(parsed[3])

  if (is.null(graph[[start]])) {
    graph[[start]] <- list()
  }
  graph[[start]][[end]] <- dist

  if (is.null(graph[[end]])) {
    graph[[end]] <- list()
  }
  graph[[end]][[start]] <- dist
}

# Add dummy city for Held-Karp
graph[["dummy"]] <- list()
for (city in names(graph)) {
  if (city != "dummy") {
    graph[["dummy"]][[city]] <- 0
    graph[[city]][["dummy"]] <- 0
  }
}

# Calculate all possible routes and their distances
all_routes <- calculate_routes(graph)

# Filter the routes based on distance
min_routes <- all_routes %>%
  filter(distance == min(all_routes$distance))

print(min_routes)

max_routes <- all_routes %>%
  filter(distance == max(all_routes$distance))
print(max_routes)

R.home() # Gives the root of the R installation directory
Sys.getenv("R_HOME") # Alternative method to get the R installation path

## If a visual representation required, graph can be created by
## uncommenting code below, readability is questionable
# Prepare data for plotting
# plot_data <- all_routes %>%
#   separate(route, into = paste0("city",
#                                 1:max(str_count(all_routes$route, "->") + 1)),
#            sep = " -> ", fill = "right") %>%
#   pivot_longer(cols = starts_with("city"),
#                names_to = "city_order", values_to = "city") %>%
#   na.omit()

# # Ensure the route is preserved in the long format
# plot_data$route <- rep(all_routes$route,
#                        each = max(str_count(all_routes$route, "->") + 1))

# # Create a base ggplot object
# base_plot <- ggplot(plot_data, aes(x = city_order,
#                                    group = route, color = route)) +
#   geom_line(aes(y = as.numeric(factor(city))),
#             alpha = 0.5, show.legend = FALSE) +
#   geom_point(aes(y = as.numeric(factor(city))), size = 3, show.legend = FALSE) +
#   labs(title = "All Possible Routes Between Cities",
#        x = "Order of Cities in Route",
#        y = "Cities") +
#   theme_minimal() +
#   scale_y_continuous(breaks = seq(1, length(unique(plot_data$city)), by = 1),
#                      labels = unique(plot_data$city)) 

# # Show the plot
# print(base_plot)
