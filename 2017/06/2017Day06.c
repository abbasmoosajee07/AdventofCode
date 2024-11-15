// # Advent of Code - Day 6, Year 2017
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2017/day/6
// # Solution by: [abbasmoosajee07]
// # Brief: [Redistribution of blocks, like candy]

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

// Function to find the maximum element in an array
int find_max(int *arr, int len) {
    int max = arr[0];
    int idx = 0;
    for (int i = 1; i < len; i++) {
        if (arr[i] > max) {
            max = arr[i];
            idx = i;
        }
    }
    return idx;
}

// Function to redistribute blocks
void redistribute_blocks(int *blocks, int len) {
    int idx = find_max(blocks, len);  // Get the index of the max block
    int max_block = blocks[idx];
    blocks[idx] = 0;  // Set the selected block to 0

    int move = 0;
    while (max_block > 0) {
        move++;
        int pos = (idx + move) % len;
        blocks[pos]++;
        max_block--;
    }
}

// Function to check if an array is present in the list of arrays
// If found, it returns the index of the array; otherwise, it returns -1
int array_in_list(int **list, int *target, int list_size, int len) {
    for (int i = 0; i < list_size; i++) {
        bool is_equal = true;
        for (int j = 0; j < len; j++) {
            if (list[i][j] != target[j]) {
                is_equal = false;
                break;
            }
        }
        if (is_equal) {
            return i;  // Return the index if arrays match
        }
    }
    return -1;
}

// Function to copy an array
void copy_array(int *src, int *dest, int len) {
    for (int i = 0; i < len; i++) {
        dest[i] = src[i];
    }
}

int main() {
    // Load input data (replace with actual file reading in production)
    // For this example, I am using an example array of integers
    int input_data[] = {10,	3,	15,	10,	5,	15,	5,	15,	9,	2,	5,	8,	5,	2,	3,	6};
    int len = sizeof(input_data) / sizeof(input_data[0]);
    int input_OG[len];

    // Copy input data to input_OG
    copy_array(input_data, input_OG, len);

    // Array to hold the history of redistributions
    int **block_list = (int **)malloc(sizeof(int *));
    block_list[0] = (int *)malloc(len * sizeof(int));
    copy_array(input_OG, block_list[0], len);

    // Variables to track progress
    int steps = 0;
    bool array_equal = false;
    int block_input[len];
    copy_array(input_OG, block_input, len);
    int list_size = 1;  // Keeps track of the size of the list of arrays
    int first_repeat_idx = -1;

    // Redistribution loop
    while (!array_equal) {
        steps++;
        // printf("Step: %d\n", steps);

        // Redistribute blocks
        redistribute_blocks(block_input, len);

        // Check if the new configuration is already in the list
        int found_idx = array_in_list(block_list, block_input, list_size, len);
        if (found_idx != -1) {  // If the configuration is found
            array_equal = true;
            first_repeat_idx = found_idx;
        } else {
            list_size++;
            block_list = (int **)realloc(block_list, list_size * sizeof(int *));
            block_list[list_size - 1] = (int *)malloc(len * sizeof(int));
            copy_array(block_input, block_list[list_size - 1], len);
        }
    }

    printf("Loop detected after %d steps.\n", steps);

    // Part 2: Calculate the loop size
    int loop_size = steps - first_repeat_idx;
    printf("Size of the loop: %d\n", loop_size);

    // Free memory
    for (int i = 0; i < list_size; i++) {
        free(block_list[i]);
    }
    free(block_list);

    return 0;
}
