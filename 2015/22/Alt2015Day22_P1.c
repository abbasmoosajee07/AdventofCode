// # Advent of Code - Day 22, Year 2015
// # Solved in 2024
// # Puzzle Link: https://adventofcode.com/2015/day/22
// # Solution by: [abbasmoosajee07]
// # Brief: [Battle Problem V2]

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#ifdef _WIN32
#include <windows.h>  // For GetModuleFileName on Windows
#else
#include <unistd.h>   // For readlink on Linux/Unix
#include <libgen.h>   // For dirname
#endif

#define LOG_SIZE 1000000  // Maximum size for the battle log

typedef struct {
    int cost;
    int damage;
    int heal;
    int armor;
    int mana_refill;
    int effect_length;
    int timer;
} Spell;

typedef struct {
    int hit_points;
    int mana_points;
    int armor;
} Wizard;

typedef struct {
    int hit_points;
    int damage;
} Boss;

// Define spells
Spell magic_missile = {53, 4, 0, 0, 0, 0, 0};
Spell drain = {73, 2, 2, 0, 0, 0, 0};
Spell shield = {113, 0, 0, 7, 0, 6, 0};
Spell poison = {173, 3, 0, 0, 0, 6, 0};
Spell recharge = {229, 0, 0, 0, 101, 5, 0};

// Array of spell names for random casting
const char *spell_list[] = {"shield", "drain", "recharge", "poison", "magic_missile"};

// Global battle log
char battle_log_P1[LOG_SIZE];
int log_index = 0;

void append_to_log(const char *message) {
    if (log_index + strlen(message) < LOG_SIZE) {
        strcpy(&battle_log_P1[log_index], message);
        log_index += strlen(message);
    }
}

const char *decide_spell(Wizard wizard, Spell spells[]) {
    while (1) {
        int random_index = rand() % 5;
        const char *cast_this_spell = spell_list[random_index];

        if (strcmp(cast_this_spell, "shield") == 0 && wizard.mana_points >= shield.cost && shield.timer == 0)
            return "shield";
        if (strcmp(cast_this_spell, "drain") == 0 && wizard.mana_points >= drain.cost)
            return "drain";
        if (strcmp(cast_this_spell, "recharge") == 0 && wizard.mana_points >= recharge.cost && recharge.timer == 0)
            return "recharge";
        if (strcmp(cast_this_spell, "poison") == 0 && wizard.mana_points >= poison.cost && poison.timer == 0)
            return "poison";
        if (strcmp(cast_this_spell, "magic_missile") == 0 && wizard.mana_points >= magic_missile.cost)
            return "magic_missile";
    }
}

void run_timer_spells(Wizard *wizard, Boss *boss) {
    char buffer[256];
    if (shield.timer > 0) {
        sprintf(buffer, "Shield active\n");
        append_to_log(buffer);
        shield.timer--;
        sprintf(buffer, "Shield timer drops to %d\n", shield.timer);
        append_to_log(buffer);
        if (shield.timer == 0) {
            sprintf(buffer, "Shield has expired, lowering wizard armor\n");
            append_to_log(buffer);
            wizard->armor -= shield.armor;
        }
    }
    if (poison.timer > 0) {
        sprintf(buffer, "Poison active\n");
        append_to_log(buffer);
        boss->hit_points -= poison.damage;
        sprintf(buffer, "Poison attacks boss for %d\n", poison.damage);
        append_to_log(buffer);
        poison.timer--;
        sprintf(buffer, "Poison timer drops to %d\n", poison.timer);
        append_to_log(buffer);
    }
    if (recharge.timer > 0) {
        sprintf(buffer, "Recharge active\n");
        append_to_log(buffer);
        wizard->mana_points += recharge.mana_refill;
        sprintf(buffer, "Mana refilled by +%d\n", recharge.mana_refill);
        append_to_log(buffer);
        recharge.timer--;
        sprintf(buffer, "Recharge drops to %d\n", recharge.timer);
        append_to_log(buffer);
    }
}

int cast_spell(Wizard *wizard, Boss *boss, const char *spell_name) {
    char buffer[256];
    if (strcmp(spell_name, "drain") == 0) {
        wizard->mana_points -= drain.cost;
        wizard->hit_points += drain.heal;
        boss->hit_points -= drain.damage;
        sprintf(buffer, "Wizard casts drain. Mana: -%d, Boss HP: -%d, Wizard HP: +%d\n", drain.cost, drain.damage, drain.heal);
        append_to_log(buffer);
        return drain.cost;
    } else if (strcmp(spell_name, "magic_missile") == 0) {
        wizard->mana_points -= magic_missile.cost;
        boss->hit_points -= magic_missile.damage;
        sprintf(buffer, "Wizard casts magic missile. Mana: -%d, Boss HP: -%d\n", magic_missile.cost, magic_missile.damage);
        append_to_log(buffer);
        return magic_missile.cost;
    } else if (strcmp(spell_name, "poison") == 0) {
        wizard->mana_points -= poison.cost;
        poison.timer = poison.effect_length;
        sprintf(buffer, "Wizard casts poison. Mana: -%d, Poison timer: %d\n", poison.cost, poison.effect_length);
        append_to_log(buffer);
        return poison.cost;
    } else if (strcmp(spell_name, "recharge") == 0) {
        wizard->mana_points -= recharge.cost;
        recharge.timer = recharge.effect_length;
        sprintf(buffer, "Wizard casts recharge. Mana: -%d, Recharge timer: %d\n", recharge.cost, recharge.effect_length);
        append_to_log(buffer);
        return recharge.cost;
    } else if (strcmp(spell_name, "shield") == 0) {
        wizard->mana_points -= shield.cost;
        wizard->armor += shield.armor;
        shield.timer = shield.effect_length;
        sprintf(buffer, "Wizard casts shield. Mana: -%d, Armor: +%d, Shield timer: %d\n", shield.cost, shield.armor, shield.effect_length);
        append_to_log(buffer);
        return shield.cost;
    }
    return 0;
}

int battle_sim(Wizard *wizard, Boss *boss) {
    int mana_spent = 0;
    char buffer[256];

    while (1) {
        sprintf(buffer, "-- Player turn --\nWizard: HP: %d, Mana: %d; Boss: %d\n", wizard->hit_points, wizard->mana_points, boss->hit_points);
        append_to_log(buffer);
        run_timer_spells(wizard, boss);
        if (wizard->mana_points <= 53 || wizard->hit_points <= 0) {
            append_to_log("Wizard is out of mana or dead!\n");
            return 0;
        }

        mana_spent += cast_spell(wizard, boss, decide_spell(*wizard, (Spell[]){shield, drain, recharge, poison, magic_missile}));

        sprintf(buffer, "-- Boss turn --\nWizard: HP: %d, Mana: %d; Boss: %d\n", wizard->hit_points, wizard->mana_points, boss->hit_points);
        append_to_log(buffer);
        run_timer_spells(wizard, boss);
        if (boss->hit_points <= 0) {
            append_to_log("Boss is dead!\n");
            return mana_spent;
        }

        int damage_taken = (boss->damage - wizard->armor > 1) ? (boss->damage - wizard->armor) : 1;
        wizard->hit_points -= damage_taken;
        sprintf(buffer, "Boss attacks for %d, Wizard HP: %d\n", damage_taken, wizard->hit_points);
        append_to_log(buffer);

        if (wizard->hit_points <= 0) {
            append_to_log("Wizard is dead!\n");
            return 0;
        }
    }
}

void save_log_to_file(const char *filename) {
    char full_path[1024];

#ifdef _WIN32
    char exe_path[MAX_PATH];
    GetModuleFileName(NULL, exe_path, MAX_PATH);
    char *last_backslash = strrchr(exe_path, '\\');
    if (last_backslash) {
        *(last_backslash + 1) = '\0';  // Truncate after last backslash
    }
    sprintf(full_path, "%s%s", exe_path, filename);
#else
    char exe_path[1024];
    ssize_t len = readlink("/proc/self/exe", exe_path, sizeof(exe_path) - 1);
    if (len != -1) {
        exe_path[len] = '\0';  // Null-terminate path
        char *dir = dirname(exe_path);
        sprintf(full_path, "%s/%s", dir, filename);
    }
#endif

    FILE *file = fopen(full_path, "w");
    if (file != NULL) {
        fputs(battle_log_P1, file);
        fclose(file);
        printf("Battle log saved to %s\n", full_path);
    } else {
        printf("Error saving battle log to file.\n");
    }
}

int main() {
    srand(time(NULL));  // Initialize random seed
    int mana_spent_to_win = __INT_MAX__;

    for (int trial = 0; trial < 100000; trial++) {
        char buffer[256];
        sprintf(buffer, "Trial: %d\n", trial);
        append_to_log(buffer);
        // Reset wizard and boss stats
        Wizard wizard = {50, 500, 0};
        Boss boss = {58, 9};

        // Reset spell timers
        shield.timer = poison.timer = recharge.timer = 0;

        int mana_spent_this_time = battle_sim(&wizard, &boss);
        if (mana_spent_this_time > 0) {
            sprintf(buffer, "Player won, spent %d mana\n", mana_spent_this_time);
            append_to_log(buffer);
            if (mana_spent_this_time < mana_spent_to_win) {
                mana_spent_to_win = mana_spent_this_time;
            }
        } else {
            sprintf(buffer, "Player lost, spent %d mana\n", mana_spent_this_time);
            append_to_log(buffer);
        }
    }

    printf("To win required %d mana.\n", mana_spent_to_win);

    char result[256];
    sprintf(result, "To win required %d mana.\n", mana_spent_to_win);
    append_to_log(result);

    save_log_to_file("battle_log_P1.txt");  // Save the log to a file

    return 0;
}
