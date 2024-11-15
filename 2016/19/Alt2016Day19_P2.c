// # Advent of Code - Day 19, Year 2016
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2016/day/19
// # Solution by: [abbasmoosajee07]
// # Brief: [Circular lists and stealing elves, P2]

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    int elf;
    int gifts;
} ElfGift;

// Function to create an array of ElfGift structs
ElfGift* create_elf_array(int no_of_elves, int gifts_per_elf) {
    ElfGift* elves = (ElfGift*)malloc(no_of_elves * sizeof(ElfGift));
    for (int i = 0; i < no_of_elves; i++) {
        elves[i].elf = i + 1;
        elves[i].gifts = gifts_per_elf;
    }
    return elves;
}

// Function to find the index of a target number in an array
int find_index(int* numbers, int length, int target_number) {
    for (int i = 0; i < length; i++) {
        if (numbers[i] == target_number) {
            return i;
        }
    }
    return -1;
}

// Function to get neighbors of a target number in a circular array
void get_neighbors(int* numbers, int length, int target_number, int* number, int* right, int* left) {
    int index = find_index(numbers, length, target_number);
    *number = numbers[index];
    *right = numbers[(index - 1 + length) % length];
    *left = numbers[(index + 1) % length];
}

// Function to find the opposite elf in a circular array
int find_opposite(int* numbers, int length, int target) {
    int target_index = find_index(numbers, length, target);
    if (target_index == -1) {
        return -1; // Target not found
    }
    int opposite_index = (target_index + (length / 2)) % length;
    if (length % 2 == 0 && (target_index + (length / 2)) % length == target_index) {
        opposite_index = target_index + (length / 2) - 1;
    }
    return numbers[opposite_index];
}

// Function to steal gifts from the opposite elf
ElfGift* steal_gifts(ElfGift* elves, int* length, int target_elf) {
    int* current_elves = (int*)malloc(*length * sizeof(int));
    for (int i = 0; i < *length; i++) {
        current_elves[i] = elves[i].elf;
    }
    
    int Elf_L = find_opposite(current_elves, *length, target_elf);
    if (Elf_L == -1) {
        free(current_elves);
        return elves;
    }

    int neighbor_elf_gifts = 0;
    for (int i = 0; i < *length; i++) {
        if (elves[i].elf == Elf_L) {
            neighbor_elf_gifts = elves[i].gifts;
            elves[i].gifts = 0;
            break;
        }
    }

    for (int i = 0; i < *length; i++) {
        if (elves[i].elf == target_elf) {
            elves[i].gifts += neighbor_elf_gifts;
            break;
        }
    }

    ElfGift* new_elves = (ElfGift*)malloc((*length - 1) * sizeof(ElfGift));
    int j = 0;
    for (int i = 0; i < *length; i++) {
        if (elves[i].elf != Elf_L) {
            new_elves[j++] = elves[i];
        }
    }
    *length -= 1;
    free(elves);
    free(current_elves);
    return new_elves;
}

int main() {
    int no_elves = 3012210; // 3012210 works for smaller numbers, takes too long for large inputs
    int gifts_per_elf = 1;
    int length = no_elves;

    ElfGift* elves = create_elf_array(no_elves, gifts_per_elf);

    int active_elf = 1;

    // Start timer
    clock_t start_time = clock();

    while (length > 1) {
        elves = steal_gifts(elves, &length, active_elf);

        int* current_elves = (int*)malloc(length * sizeof(int));
        for (int i = 0; i < length; i++) {
            current_elves[i] = elves[i].elf;
        }

        int number, right, left;
        get_neighbors(current_elves, length, active_elf, &number, &right, &left);
        // printf("active elf %d \n", active_elf);

        active_elf = left;
        free(current_elves);
    }

    // Stop timer
    clock_t end_time = clock();
    double time_taken = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    printf("The properties of the remaining elf\nElf: %d, Gifts: %d\n", elves[0].elf, elves[0].gifts);
    printf("Time taken: %f seconds\n", time_taken);

    free(elves);
    return 0;
}
