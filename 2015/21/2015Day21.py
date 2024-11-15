# Advent of Code - Day 21, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/21
# Solution by: [abbasmoosajee07]
# Brief: [Role Playing Battle]

import os, re
from itertools import product

# Defining the weapon, armor, and ring data
WEAPONS = {
    "Dagger": {"cost": 8, "Damage": 4, "armor": 0},
    "Shortsword": {"cost": 10, "Damage": 5, "armor": 0},
    "Warhammer": {"cost": 25, "Damage": 6, "armor": 0},
    "Longsword": {"cost": 40, "Damage": 7, "armor": 0},
    "Greataxe": {"cost": 74, "Damage": 8, "armor": 0}
}

ARMOR = {
    "None": {"cost": 0, "Damage": 0, "armor": 0},  # Adding a 'No Armor' option
    "Leather": {"cost": 13, "Damage": 0, "armor": 1},
    "Chainmail": {"cost": 31, "Damage": 0, "armor": 2},
    "Splintmail": {"cost": 53, "Damage": 0, "armor": 3},
    "Bandedmail": {"cost": 75, "Damage": 0, "armor": 4},
    "Platemail": {"cost": 102, "Damage": 0, "armor": 5}
}

RINGS = {
    "None": {"cost": 0, "Damage": 0, "armor": 0},  # Adding a 'No Ring' option
    "Damage +1": {"cost": 25, "Damage": 1, "armor": 0},
    "Damage +2": {"cost": 50, "Damage": 2, "armor": 0},
    "Damage +3": {"cost": 100, "Damage": 3, "armor": 0},
    "Defense +1": {"cost": 20, "Damage": 0, "armor": 1},
    "Defense +2": {"cost": 40, "Damage": 0, "armor": 2},
    "Defense +3": {"cost": 80, "Damage": 0, "armor": 3}
}

# Unified data structure
EQUIPMENT = {
    "Weapons": {},
    "Armor": {},
    "Rings": {}
}

def parse_line(line):
    """Parse a line from the text file and return a tuple of name and attributes."""
    parts = re.split(r'\s{2,}', line.strip())
    name = parts[0]
    cost, Damage, armor = map(int, parts[1:])
    return name, {"cost": cost, "Damage": Damage, "armor": armor}

def read_equipment_from_file(file_path):
    """Read equipment data from a text file and populate the EQUIPMENT dictionary."""
    with open(file_path, 'r') as file:
        current_category = None
        for line in file:
            line = line.strip()
            if line.startswith("Weapons:"):
                current_category = "Weapons"
                continue
            elif line.startswith("Armor:"):
                current_category = "Armor"
                continue
            elif line.startswith("Rings:"):
                current_category = "Rings"
                continue
            
            if current_category and line:
                name, attributes = parse_line(line)
                EQUIPMENT[current_category][name] = attributes

# Call this function with the path to your text file
D21_shop_file = 'Day21_shop.txt'
D21_shop_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_shop_file)
read_equipment_from_file(D21_shop_file_path)

D21_file = 'Day21_input.txt'
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

with open(D21_file_path) as file:
    input_data = file.read().splitlines()

hit_points = input_data[0].split(': ')[1]
damage = input_data[1].split(': ')[1]
armor = input_data[2].split(': ')[1]

BOSS_POINTS = {'Hit Points': int(hit_points), 'Damage': int(damage), 'armor': int(armor)}

# ---------------------------------------------------------------------------
# Generating combinations of equipment
weapons = [key for key in WEAPONS.keys()]
armor = [key for key in ARMOR.keys()]
left_hand = [key for key in RINGS.keys()]
right_hand = [key for key in RINGS.keys()]

# Filter out combinations where both rings are the same
all_battle_combinations = [combo for combo in product(weapons, armor, left_hand, right_hand) if combo[2] != combo[3]]

def battle_sim(player: dict, enemy: dict) -> bool:
    """Simulate a battle and return true if the player wins."""
    while True:
        # Player attacks boss
        enemy_Damage_taken = max(1, player['Damage'] - enemy["armor"])  # Player deals at least 1 Damage
        enemy["Hit Points"] -= enemy_Damage_taken
        
        if enemy["Hit Points"] <= 0:
            return True  # Player wins
        
        # Boss attacks player
        player_Damage_taken = max(1, enemy['Damage'] - player['armor'])  # Boss deals at least 1 Damage
        player['Hit Points'] -= player_Damage_taken
        
        if player["Hit Points"] <= 0:
            return False  # Boss wins

def equip_player(equipment: tuple) -> dict:
    """Determine the equipment the player is wearing and the cost. Output is a player dict."""
    return {
        'Hit Points': 100,
        'Damage': (
            WEAPONS[equipment[0]]['Damage']
            + ARMOR[equipment[1]]['Damage']
            + RINGS[equipment[2]]['Damage']
            + RINGS[equipment[3]]['Damage']
        ),
        'armor': (
            WEAPONS[equipment[0]]['armor']
            + ARMOR[equipment[1]]['armor']
            + RINGS[equipment[2]]['armor']
            + RINGS[equipment[3]]['armor']
        ),
        'cost': (
            WEAPONS[equipment[0]]['cost']
            + ARMOR[equipment[1]]['cost']
            + RINGS[equipment[2]]['cost']
            + RINGS[equipment[3]]['cost']
        ),
    }


cost_to_win = float('inf')
cost_to_lose = 0

for combination in all_battle_combinations:
    player = equip_player(combination)
    BOSS = BOSS_POINTS.copy()  # Reset BOSS stats for each battle
    
    if battle_sim(player, BOSS):
        if player['cost'] < cost_to_win:
            cost_to_win = player['cost']
    else:
        if player['cost'] > cost_to_lose:
            cost_to_lose = player['cost']

print(f"\nPart 1: The least gold that can be spent to win is {cost_to_win}.")
print(f"\nPart 2: The most gold that can be spent and still lose is {cost_to_lose}.")
