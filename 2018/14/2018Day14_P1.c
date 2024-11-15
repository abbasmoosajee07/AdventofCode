// # Advent of Code - Day 14, Year 2018
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2018/day/14
// # Solution by: [abbasmoosajee07]
// # Brief: [Perfect Chocolate Recipe]

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RECIPES 11414140

typedef struct {
    int* recipes;
    int elf1;
    int elf2;
    int size;
} RecipeState;

void append_recipe(RecipeState* state, int score) {
    if (state->size >= MAX_RECIPES) {
        printf("Exceeded max recipes size.\n");
        exit(1);
    }
    state->recipes[state->size++] = score;
}

RecipeState calc_recipe_score(RecipeState state) {
    int recipe1 = state.recipes[state.elf1];
    int recipe2 = state.recipes[state.elf2];

    int total_score = recipe1 + recipe2;
    if (total_score >= 10) {
        append_recipe(&state, total_score / 10);
    }
    append_recipe(&state, total_score % 10);

    state.elf1 = (state.elf1 + 1 + recipe1) % state.size;
    state.elf2 = (state.elf2 + 1 + recipe2) % state.size;

    return state;
}

int main() {
    int generations = 540561; // Puzzle INput
    RecipeState state;
    state.size = 2;
    state.recipes = malloc(MAX_RECIPES * sizeof(int));
    state.recipes[0] = 3;
    state.recipes[1] = 7;
    state.elf1 = 0;
    state.elf2 = 1;

    for (int i = 0; i < generations + 20; i++) {
        state = calc_recipe_score(state);
    }

    char final_score[11];
    for (int i = 0; i < 10; i++) {
        final_score[i] = state.recipes[generations + i] + '0';
    }
    final_score[10] = '\0';
    
    printf("Part 1: Score of next 10 recipes is %s\n", final_score);

    free(state.recipes);
    return 0;
}
