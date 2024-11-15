# Advent of Code - Day 22, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Battle Problem V2]

require 'securerandom'

# Spells
magic_missile = { cost: 53, damage: 4 }
drain = { cost: 73, damage: 2, heal: 2 }
shield = { cost: 113, armor: 7, effect_length: 6, timer: 0 }
poison = { cost: 173, damage: 3, effect_length: 6, timer: 0 }
recharge = { cost: 229, mana_refill: 101, effect_length: 5, timer: 0 }

wizard = { hit_points: 50, mana_points: 500, armor: 0 }
boss = { hit_points: 58, damage: 9 }

def decide_spell(wizard, spells)
  spell_list = %w[shield drain recharge poison magic_missile]
  loop do
    cast_this_spell = spell_list.sample
    case cast_this_spell
    when "shield"
      return "shield" if wizard[:mana_points] >= spells[:shield][:cost] && spells[:shield][:timer].zero?
    when "drain"
      return "drain" if wizard[:mana_points] >= spells[:drain][:cost]
    when "recharge"
      return "recharge" if wizard[:mana_points] >= spells[:recharge][:cost] && spells[:recharge][:timer].zero?
    when "poison"
      return "poison" if wizard[:mana_points] >= spells[:poison][:cost] && spells[:poison][:timer].zero?
    when "magic_missile"
      return "magic_missile" if wizard[:mana_points] >= spells[:magic_missile][:cost]
    end
  end
end

def run_timer_spells(wizard, boss, spells)
  if spells[:shield][:timer] > 0
    # puts "Shield active"
    spells[:shield][:timer] -= 1
    # puts "Shield timer drops to #{spells[:shield][:timer]}"
    if spells[:shield][:timer].zero?
      # puts "Shield has expired, lowering wizard armor"
      wizard[:armor] -= spells[:shield][:armor]
    end
  end
  if spells[:poison][:timer] > 0
    # puts "Poison active"
    boss[:hit_points] -= spells[:poison][:damage]
    # puts "Poison attacks boss for #{spells[:poison][:damage]}"
    spells[:poison][:timer] -= 1
    # puts "Poison timer drops to #{spells[:poison][:timer]}"
  end
  if spells[:recharge][:timer] > 0
    # puts "Recharge active"
    wizard[:mana_points] += spells[:recharge][:mana_refill]
    # puts "Mana refilled by +#{spells[:recharge][:mana_refill]}"
    spells[:recharge][:timer] -= 1
    # puts "Recharge drops to #{spells[:recharge][:timer]}"
  end
end

def cast_spell(wizard, boss, spell_name, spells)
  case spell_name
  when "drain"
    wizard[:mana_points] -= spells[:drain][:cost]
    wizard[:hit_points] += spells[:drain][:heal]
    boss[:hit_points] -= spells[:drain][:damage]
    return spells[:drain][:cost]
  when "magic_missile"
    wizard[:mana_points] -= spells[:magic_missile][:cost]
    boss[:hit_points] -= spells[:magic_missile][:damage]
    return spells[:magic_missile][:cost]
  when "poison"
    wizard[:mana_points] -= spells[:poison][:cost]
    spells[:poison][:timer] = spells[:poison][:effect_length]
    return spells[:poison][:cost]
  when "recharge"
    wizard[:mana_points] -= spells[:recharge][:cost]
    spells[:recharge][:timer] = spells[:recharge][:effect_length]
    return spells[:recharge][:cost]
  when "shield"
    wizard[:mana_points] -= spells[:shield][:cost]
    wizard[:armor] += spells[:shield][:armor]
    spells[:shield][:timer] = spells[:shield][:effect_length]
    return spells[:shield][:cost]
  end
end

def battle_sim(wizard, boss, spells)
  mana_spent = 0
  loop do
    # puts "--player turn--"
    # puts "Wizard: HP: #{wizard[:hit_points]}, Mana: #{wizard[:mana_points]}; Boss: #{boss[:hit_points]}"
    run_timer_spells(wizard, boss, spells)
    return [false, mana_spent] if wizard[:mana_points] <= 53 || wizard[:hit_points] <= 0
    
    mana_spent += cast_spell(wizard, boss, decide_spell(wizard, spells), spells)
    
    # Boss turn
    # puts "--boss turn--"
    # puts "Wizard: HP: #{wizard[:hit_points]}, Mana: #{wizard[:mana_points]}; Boss: #{boss[:hit_points]}"
    run_timer_spells(wizard, boss, spells)
    # puts "Boss attacks #{boss[:damage]}"
    return [true, mana_spent] if boss[:hit_points] <= 0
    
    wizard[:hit_points] -= [boss[:damage] - wizard[:armor], 1].max # prevent negative damage
    return [false, mana_spent] if wizard[:hit_points] <= 0
  end
end

spells = {
  magic_missile: magic_missile,
  drain: drain,
  shield: shield,
  poison: poison,
  recharge: recharge
}

if __FILE__ == $0
  mana_spent_to_win = Float::INFINITY
  100_000.times do |trial|
    # puts "Trial: #{trial}"  # Changed to be compatible with older Ruby versions
    # Reset wizard and boss stats
    wizard = { hit_points: 50, mana_points: 500, armor: 0 }
    boss = { hit_points: 58, damage: 9 }
    
    # Reset spell timers
    spells[:shield][:timer] = 0
    spells[:poison][:timer] = 0
    spells[:recharge][:timer] = 0
    
    did_player_win, mana_spent_this_time = battle_sim(wizard, boss, spells)
    if did_player_win
      # puts "Player won, spent #{mana_spent_this_time} mana"
      mana_spent_to_win = [mana_spent_to_win, mana_spent_this_time].min
    else
      # puts "Player lost, spent #{mana_spent_this_time} mana"
    end
  end
  puts "To win required #{mana_spent_to_win} mana."
end
