import re
from sys import path


D14_file = 'Day14_reindeer.txt'
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

with open(D14_file_path) as file:
    reindeer_race = file.read()
    
reindeer_race = reindeer_race.splitlines()
class Reindeer:
    def __init__(self, speed, flying_time, resting_time):
        self.speed = speed
        self.flying_time = flying_time
        self.original_flying_time = flying_time
        self.resting_time = resting_time
        self.original_resting_time = resting_time
        self.total_distance = 0
        self.points = 0

    def move(self):
        if self.resting_time == 0:
            self.flying_time = self.original_flying_time
            self.resting_time = self.original_resting_time
        if self.flying_time > 0:
            self.total_distance += self.speed
            self.flying_time -= 1
        elif self.resting_time > 0:
            self.resting_time -= 1

    def __gt__(self, other):
        return self.total_distance > other.total_distance


def figure_out_reindeer_specs(line):
    regex = re.compile(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.')
    results = re.findall(regex, line)
    reindeer_name, speed, fly_time, rest_time = results[0][0], results[0][1], results[0][2], results[0][3]
    return reindeer_name, int(speed), int(fly_time), int(rest_time)


def create_reindeer_list(attribute_list):
    reindeer_list = []
    for reindeer in attribute_list:
        reindeer_name, speed, fly_time, rest_time = figure_out_reindeer_specs(reindeer)
        reindeer_list.append(Reindeer(speed, fly_time, rest_time))
    return reindeer_list


def move_and_assign_points(list_of_reindeer, total_seconds):
    time = 0
    while time < total_seconds + 1:
        for reindeer in list_of_reindeer:
            reindeer.move()
        list_of_reindeer = sorted(list_of_reindeer)
        current_top_distance = list_of_reindeer[-1].total_distance
        for reindeer in list_of_reindeer:
            if reindeer.total_distance == current_top_distance:
                reindeer.points += 1
        time += 1


if __name__ == "__main__":
    reindeer_attributes = reindeer_race
    all_reindeer = create_reindeer_list(reindeer_attributes)
    move_and_assign_points(all_reindeer, 2503)
    highest_points = 0
    for reindeer in all_reindeer:
        if reindeer.points > highest_points:
            highest_points = reindeer.points
    print(f"The highest-scoring reindeer got {highest_points} points.")

