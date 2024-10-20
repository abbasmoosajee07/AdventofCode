# SmallBitSet module to simulate the functionality of Haskell's SmallBitSet
class SmallBitSet
    def initialize(elements = [])
      @set = elements.uniq.sort
    end
  
    def self.from_list(elements)
      new(elements)
    end
  
    def empty?
      @set.empty?
    end
  
    def to_list
      @set
    end
  
    def union(other)
      SmallBitSet.new(@set | other.to_list)
    end
  
    def difference(other)
      SmallBitSet.new(@set - other.to_list)
    end
  
    def intersection(other)
      SmallBitSet.new(@set & other.to_list)
    end
  
    def set_rep(shift_amount)
      # Simplified version of setRep using bitwise operations
      @set.reduce(0) { |acc, el| acc | (1 << (el + shift_amount)) }
    end
  end
  
  # Floor class to represent a floor in the building
  class Floor
    attr_reader :gens, :mics
  
    def initialize(gens, mics)
      @gens = gens
      @mics = mics
    end
  
    def empty?
      @gens.empty? && @mics.empty?
    end
  
    def valid?
      @gens.empty? || @mics.difference(@gens).empty?
    end
  
    def union(other)
      Floor.new(@gens.union(other.gens), @mics.union(other.mics))
    end
  
    def difference(other)
      Floor.new(@gens.difference(other.gens), @mics.difference(other.mics))
    end
  
    def self.pick_from_floor(floor)
      gens = floor.gens.to_list
      mics = floor.mics.to_list
      pick2(gens).map { |pair| Floor.new(SmallBitSet.from_list(pair), SmallBitSet.new) } +
        pick2(mics).map { |pair| Floor.new(SmallBitSet.new, SmallBitSet.from_list(pair)) } +
        gens.map { |g| Floor.new(SmallBitSet.from_list([g]), SmallBitSet.new) } +
        mics.map { |m| Floor.new(SmallBitSet.new, SmallBitSet.from_list([m])) }
    end
  
    def self.pick2(list)
      list.combination(2).to_a
    end
  
    def rep
      gens.set_rep(7) | mics.set_rep(0)
    end
  end
  
  # Building class to represent the entire building
  class Building
    attr_accessor :steps, :lower_floors, :current_floor, :higher_floors
  
    def initialize(steps, lower_floors, current_floor, higher_floors)
      @steps = steps
      @lower_floors = lower_floors
      @current_floor = current_floor
      @higher_floors = higher_floors
    end
  
    def solved?
      higher_floors.empty? && lower_floors.all?(&:empty?)
    end
  
    def advance_building
      new_buildings = []
  
      Floor.pick_from_floor(current_floor).each do |subset|
        update_current_floor(lambda { |f| f.difference(subset) }) do |b1|
          move(:lower_floors, :higher_floors, b1).each do |b2|
            move(:higher_floors, :lower_floors, b1).each do |b3|
              update_current_floor(lambda { |f| f.union(subset) }) do |b4|
                b4.steps += 1
                new_buildings << b4
              end
            end
          end
        end
      end
  
      new_buildings
    end
  
    def update_current_floor(transform)
      new_floor = transform.call(current_floor)
      if new_floor.valid?
        new_building = self.clone
        new_building.current_floor = new_floor
        yield new_building if block_given?
      end
    end
  
    def move(back_floors, front_floors, building)
      next_buildings = []
      current_floors = building.send(front_floors)
  
      if current_floors.any?
        next_buildings << building.clone.tap do |b|
          b.send(back_floors).unshift(building.current_floor)
          b.current_floor = current_floors.first
          b.send(front_floors).shift
        end
      end
  
      next_buildings
    end
  
    def rep
      (lower_floors.size << 14) | (lower_floors + higher_floors).reduce(0) { |acc, fl| acc << 14 | fl.rep }
    end
  end
  
  # Main logic and parameters
  def part1
    Building.new(0, [], mk_floor([0], [0]), [mk_floor([1, 2, 3, 4], []), mk_floor([], [1, 2, 3, 4]), mk_floor([], [])])
  end
  
  def part2
    Building.new(0, [], mk_floor([0, 1, 2], [0, 1, 2]), [mk_floor([3, 4, 5, 6], []), mk_floor([], [3, 4, 5, 6]), mk_floor([], [])])
  end
  
  def solution_steps(building)
    queue = [[building, 0]]
  
    until queue.empty?
      current_building, steps = queue.shift
  
      if current_building.solved?
        return steps
      end
  
      current_building.advance_building.each do |new_building|
        queue.push([new_building, steps + 1])
      end
    end
  
    nil
  end
  
  def mk_floor(gens, mics)
    Floor.new(SmallBitSet.from_list(gens), SmallBitSet.from_list(mics))
  end
  
  puts solution_steps(part1)
  puts solution_steps(part2)
  