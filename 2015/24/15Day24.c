#include <stdio.h>
#include <stdlib.h>

#define MAX_COMBOS 10000
#define INF 1000000000000000000

// Function to calculate the sum of an array
int array_sum(int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

// Function to calculate the product of an array
long long array_product(int arr[], int size) {
    long long product = 1;
    for (int i = 0; i < size; i++) {
        product *= arr[i];
    }
    return product;
}

// Recursive function to find combinations
void find_combinations(int packages[], int size, int start, int combo[], int combo_size, int sum, int target_sum, int result[][MAX_COMBOS], int *result_count) {
    if (sum == target_sum) {
        for (int i = 0; i < combo_size; i++) {
            result[*result_count][i] = combo[i];
        }
        (*result_count)++;
        return;
    }
    if (sum > target_sum) return;

    for (int i = start; i < size; i++) {
        combo[combo_size] = packages[i];
        find_combinations(packages, size, i + 1, combo, combo_size + 1, sum + packages[i], target_sum, result, result_count);
    }
}

// Main function to create package combinations
void create_package_combo(int packages[], int size, int group_no) {
    int total_sum = array_sum(packages, size);
    int target_sum = total_sum / group_no;

    int result[MAX_COMBOS][size];
    int result_count = 0;
    int combo[size];

    find_combinations(packages, size, 0, combo, 0, 0, target_sum, result, &result_count);

    int min_length = INF;
    for (int i = 0; i < result_count; i++) {
        int length = 0;
        while (result[i][length] != 0 && length < size) length++;
        if (length < min_length) {
            min_length = length;
        }
    }

    long long min_quantum_entanglement = INF;
    for (int i = 0; i < result_count; i++) {
        int length = 0;
        while (result[i][length] != 0 && length < size) length++;
        if (length == min_length) {
            long long quantum_entanglement = array_product(result[i], length);
            if (quantum_entanglement < min_quantum_entanglement) {
                min_quantum_entanglement = quantum_entanglement;
            }
        }
    }

    printf("The quantum entanglement of the packages organised in %d groups is %lld\n", group_no, min_quantum_entanglement);
}

int main() {
    int packages_input[] = {1, 2, 3, 7, 11, 13, 17, 19, 23, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113};
    int size = sizeof(packages_input) / sizeof(packages_input[0]);

    // Part 1: Group into 3 groups
    create_package_combo(packages_input, size, 3);

    // Part 2: Group into 4 groups
    create_package_combo(packages_input, size, 4);

    return 0;
}

