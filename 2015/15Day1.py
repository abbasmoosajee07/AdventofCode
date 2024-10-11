file_path = '2015\Data Files\Floors.txt'
# Read the file and print its content
with open(file_path) as file:
    floors = file.read()
    
print(floors)

print(len(floors))