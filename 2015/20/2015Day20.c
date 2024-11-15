// # Advent of Code - Day 20, Year 2015
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2015/day/20
// # Solution by: [abbasmoosajee07]
// # Brief: [Circular Travelling Salesman Problem]

#include <stdio.h>
#include <stdlib.h>

#define TARGET 36000000
#define MAX_HOUSES 1000000 // Arbitrarily large number to cover enough houses

void find_house_part_1(int *houses, int target, int multiplier) {
    // Elves deliver presents to all their multiples, with each elf delivering "multiplier * elf_number"
    for (int elf = 1; elf < MAX_HOUSES; elf++) {
        for (int house = elf; house < MAX_HOUSES; house += elf) {
            houses[house] += elf * multiplier;
        }
    }

    // Find the lowest house that gets at least the target number of presents
    for (int i = 1; i < MAX_HOUSES; i++) {
        if (houses[i] >= target) {
            printf("Part 1: The lowest house number to get at least %d presents is: %d\n", target, i);
            break;
        }
    }
}

void find_house_part_2(int *houses, int target, int multiplier, int max_visits) {
    // Elves deliver presents to a maximum of `max_visits` houses, delivering "multiplier * elf_number"
    for (int elf = 1; elf < MAX_HOUSES; elf++) {
        int visits = 0;
        for (int house = elf; house < MAX_HOUSES && visits < max_visits; house += elf) {
            houses[house] += elf * multiplier;
            visits++;
        }
    }

    // Find the lowest house that gets at least the target number of presents
    for (int i = 1; i < MAX_HOUSES; i++) {
        if (houses[i] >= target) {
            printf("Part 2: The lowest house number to get at least %d presents is: %d\n", target, i);
            break;
        }
    }
}

int main() {
    // Allocate memory for the house arrays
    int *houses_part_1 = (int *)calloc(MAX_HOUSES, sizeof(int));
    int *houses_part_2 = (int *)calloc(MAX_HOUSES, sizeof(int));

    // Part 1: Elves deliver to all multiples, each delivering 10 times their number
    find_house_part_1(houses_part_1, TARGET, 10);

    // Part 2: Elves deliver to 50 houses max, each delivering 11 times their number
    find_house_part_2(houses_part_2, TARGET, 11, 50);

    // Clean up allocated memory
    free(houses_part_1);
    free(houses_part_2);

    return 0;
}
