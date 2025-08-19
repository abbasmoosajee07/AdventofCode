// # Advent of Code - Day 19, Year 2016
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2016/day/19
// # Solution by: [abbasmoosajee07]
// # Brief: [Circular lists and stealing elves, P1]

#include <stdio.h>
#include <stdlib.h>

// Function to initialize an array of elves with one gift each
int* create_elves(int no_of_elves) {
    int* elves = (int*)malloc(no_of_elves * sizeof(int));
    for (int i = 0; i < no_of_elves; i++) {
        elves[i] = 1;  // Each elf starts with 1 gift
    }
    return elves;
}

// Function to find the next elf (left neighbor) in a circular list
int get_next_elf(int current_elf, int total_elves, int* elves) {
    int next_elf = (current_elf + 1) % total_elves;
    while (elves[next_elf] == 0) {  // Skip elves that have been removed (i.e., elves with 0 gifts)
        next_elf = (next_elf + 1) % total_elves;
    }
    return next_elf;
}

// Main function to simulate the elves stealing gifts game
int main() {
    int no_of_elves = 3012210;  // Total number of elves Your Input
    int* elves = create_elves(no_of_elves);  // Create the elves array
    
    int active_elf = 0;  // Start with the first elf (index 0)
    int remaining_elves = no_of_elves;  // Track how many elves are left
    
    // Continue until only one elf remains
    while (remaining_elves > 1) {
        // Find the elf to the left (in a circular manner)
        int target_elf = get_next_elf(active_elf, no_of_elves, elves);
        
        // Steal gifts from the left neighbor
        elves[active_elf] += elves[target_elf];
        elves[target_elf] = 0;  // The target elf is now out (gifts stolen)
        
        remaining_elves--;  // Decrease the number of remaining elves
        
        // Move to the next elf (circularly)
        active_elf = get_next_elf(active_elf, no_of_elves, elves);
    }
    
    // Find the last remaining elf
    for (int i = 0; i < no_of_elves; i++) {
        if (elves[i] > 0) {
            printf("The last elf remaining is: Elf %d\n", i + 1);
            break;
        }
    }
    
    free(elves);  // Free the allocated memory
    return 0;
}
