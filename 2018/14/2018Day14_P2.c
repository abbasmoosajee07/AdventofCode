// # Advent of Code - Day 14, Year 2018
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2018/day/14
// # Solution by: [abbasmoosajee07]
// # Brief: [Perfect Chocolate Recipe]

#include <stdio.h>
#include <stdlib.h>

int main() {
    int value = 540561;   // Puzzle input value
    int digits[10];     // Array to hold individual digits of the value
    int num_digits = 0;
    int temp = value;

    // Convert the integer value to an array of digits
    while (temp > 0) {
        digits[num_digits++] = temp % 10;
        temp /= 10;
    }

    // Reverse the digits array since we built it backwards
    for (int i = 0; i < num_digits / 2; i++) {
        int swap = digits[i];
        digits[i] = digits[num_digits - i - 1];
        digits[num_digits - i - 1] = swap;
    }

    // Initialize the scoreboard and the elves' positions
    int *scores = malloc(2 * sizeof(int));
    int score_count = 2;
    scores[0] = 3;
    scores[1] = 7;
    int elf1 = 0, elf2 = 1;
    int capacity = 2;  // Track the capacity of the dynamic array

    int found = 0;
    while (!found) {
        // Calculate new recipes and append to the scoreboard
        int total = scores[elf1] + scores[elf2];
        if (total >= 10) {
            if (score_count + 1 >= capacity) {
                capacity *= 2;
                scores = realloc(scores, capacity * sizeof(int));
            }
            scores[score_count++] = total / 10;
        }
        
        if (score_count >= capacity) {
            capacity *= 2;
            scores = realloc(scores, capacity * sizeof(int));
        }
        scores[score_count++] = total % 10;

        // Update the elves' positions
        elf1 = (elf1 + 1 + scores[elf1]) % score_count;
        elf2 = (elf2 + 1 + scores[elf2]) % score_count;

        // Check if the last `num_digits` or `num_digits + 1` match the sequence
        if (score_count >= num_digits) {
            found = 1;
            for (int i = 0; i < num_digits; i++) {
                if (scores[score_count - num_digits + i] != digits[i]) {
                    found = 0;
                    break;
                }
            }
            if (found) break;
        }
        if (score_count >= num_digits + 1) {
            found = 1;
            for (int i = 0; i < num_digits; i++) {
                if (scores[score_count - num_digits - 1 + i] != digits[i]) {
                    found = 0;
                    break;
                }
            }
            if (found) {
                score_count--;  // Adjust if sequence was found one position back
                break;
            }
        }
    }

    // Output the result
    printf("Number of recipes before sequence: %d\n", score_count - num_digits);

    // Free allocated memory
    free(scores);

    return 0;
}
