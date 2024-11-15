// # Advent of Code - Day 15, Year 2017
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2017/day/15
// # Solution by: [abbasmoosajee07]
// # Brief: [Syncing Generators, P2]

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define FACTOR_A 16807
#define FACTOR_B 48271
#define DIVIDER 2147483647
#define PAIRS_CREATED 5000000 // Use 40000000 for full run

// Function to get the lowest 16 bits of a value
uint16_t lowest_16_bits(uint32_t value) {
    return value & 0xFFFF;
}

// Function to generate the next value for generator A that is a multiple of 4
uint32_t produce_gen_A(uint32_t gen_A) {
    while (true) {
        gen_A = ((uint64_t)gen_A * FACTOR_A) % DIVIDER;
        if (gen_A % 4 == 0) {
            return gen_A;
        }
    }
}

// Function to generate the next value for generator B that is a multiple of 8
uint32_t produce_gen_B(uint32_t gen_B) {
    while (true) {
        gen_B = ((uint64_t)gen_B * FACTOR_B) % DIVIDER;
        if (gen_B % 8 == 0) {
            return gen_B;
        }
    }
}

int main() {
    uint32_t gen_A = 634;       // Initial value for generator A
    uint32_t gen_B = 301;      // Initial value for generator B
    int match_pairs = 0;        // Counter for matching pairs

    // Loop through the number of pairs to be created
    for (int i = 0; i < PAIRS_CREATED; i++) {
        gen_A = produce_gen_A(gen_A);
        gen_B = produce_gen_B(gen_B);

        // Get the lowest 16 bits of each generator value
        uint16_t bin_A = lowest_16_bits(gen_A);
        uint16_t bin_B = lowest_16_bits(gen_B);

        // Check if the lowest 16 bits match
        if (bin_A == bin_B) {
            match_pairs ++;
        }
    }

    printf("Part 2: Number of matching pairs: %d\n", match_pairs);
    return 0;
}
