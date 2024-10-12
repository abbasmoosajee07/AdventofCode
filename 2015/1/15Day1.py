import sys 
import os 

script_directory = os.path.dirname(os.path.abspath(__file__))

# Set the working directory to the script's directory
os.chdir(script_directory)
print(script_directory)

D1_file = 'Day1_Floors.txt'
D1_file_path = os.path.join(script_directory, D1_file)
print(D1_file_path)

print(os.path.dirname(os.path.abspath(__file__)))

# # Read the file and print its content
# with open(D1_file_path) as file:
#     apt = file.read()
    
# floor_list = list(apt)
    
# total_floors = len(apt)

# # Initialize a counter at ground floor = 0
# floor_i = 0
# basement_indices = []

# # Iterate through the whole apartment counting the floors as it goes along
# for i in range(total_floors):

#     if floor_i == -1:
#         basement_indices.append(i)

#     # Check if the bracket is (
#     if floor_list[i] == '(': 
#         floor_i += 1
#     else:
#         floor_i += -1
    

# print(f"Instructions direct Santa to Floor {floor_i}.")

# print(f"Santa first enters basement at position {basement_indices[0]}.")

