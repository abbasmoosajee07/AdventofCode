// # Advent of Code - Day 15, Year 2017
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2017/day/15
// # Solution by: [abbasmoosajee07]
// # Brief: [Syncing Generators, P1]

#include <stdio.h>
#include <stdint.h>

#define FACTOR_A 16807
#define FACTOR_B 48271
#define DIVIDER 2147483647
#define PAIRS_CREATED 40000000

// Function to calculate the lowest 16 bits
uint16_t lowest_16_bits(uint32_t value) {
    return value & 0xFFFF;  // Mask to get only the lowest 16 bits
}

// Function to produce generator values for A and B
void produce_gen_values(uint32_t *gen_A, uint32_t *gen_B) {
    *gen_A = ((uint64_t)(*gen_A) * FACTOR_A) % DIVIDER;
    *gen_B = ((uint64_t)(*gen_B) * FACTOR_B) % DIVIDER;
}

int main() {
    uint32_t gen_A = 634;      // Initial value for generator A
    uint32_t gen_B = 301;     // Initial value for generator B
    int match_pairs = 0;       // Counter for matched pairs

    for (int i = 0; i < PAIRS_CREATED; i++) {
        // Produce the next values for generators A and B
        produce_gen_values(&gen_A, &gen_B);

        // Get the lowest 16 bits of each generator
        uint16_t bin_A = lowest_16_bits(gen_A);
        uint16_t bin_B = lowest_16_bits(gen_B);

        // Check if the lowest 16 bits match
        if (bin_A == bin_B) {
            match_pairs++;
        }
    }

    printf("Part 1: Number of matching pairs: %d\n", match_pairs);
    return 0;
}