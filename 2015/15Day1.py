file_path = '2015\Data Files\Day1_Floors.txt'
# Read the file and print its content
with open(file_path) as file:
    apt = file.read()
    
floor_list = list(apt)
    
total_floors = len(apt)

# Initialize a counter at ground floor = 0
floor_i = 0
basement_indices = []

# Iterate through the whole apartment counting the floors as it goes along
for i in range(total_floors):

    if floor_i == -1:
        basement_indices.append(i)

    # Check if the bracket is (
    if floor_list[i] == '(': 
        floor_i += 1
    else:
        floor_i += -1
    

print(f"Instructions direct Santa to Floor {floor_i}.")

print(f"Santa first enters basement at position {basement_indices[0]}.")

