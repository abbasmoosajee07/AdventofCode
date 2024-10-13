import os
import numpy as np

D9_file = 'Day9_routes.txt'
D9_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D9_file)

with open(D9_file_path) as file:
    routes_list = file.read()

routes_list = routes_list.splitlines()

print(routes_list)

