import random
import pandas as pd

def make_uniform_fd(x,y,max_uniform_force_density, min_uniform_force_density, increment_uniform_force_density, iterations, mesh_number_positioning):
    '''
    # DESCRIPTION: makes a list of uniform force_densities where the mesh id is random
    # INPUT: x,y, max_uniform_force_density, min_uniform_force_density, increment_uniform_force_density, iterations, mesh_number_positioning
      mesh number positioning is either 'consecutive' or 'random'
    # OUTPUT: 
            example: mesh_2033': [[4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6], [4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6, 4.6]], 'mesh_5680':[[4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7], [4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7, 4.7]]
    '''



    list_counter = []
    counter = min_uniform_force_density
    while counter <= max_uniform_force_density:
        list_counter.append(round(counter,1))
        counter+=increment_uniform_force_density
    # print(list_counter)

    uniform_fd_meshes = []
    for number in list_counter:
        row_uniform = [number]*(x+1)
        col_uniform = [number]*(y+1)
        uniform_fd_meshes.append([row_uniform,col_uniform])

    random_mesh_numbers = random.sample(range(1,iterations), len(uniform_fd_meshes))
    consecutive_mesh_numbers = list(range(0,len(uniform_fd_meshes)))  

    if mesh_number_positioning == 'random':
        mesh_numbers = random_mesh_numbers
    elif mesh_number_positioning == 'consecutive':
        mesh_numbers = consecutive_mesh_numbers

    uniform_fd_mesh_dict = {}
    for i, val in enumerate(uniform_fd_meshes):
        uniform_fd_mesh_dict[f'mesh_{mesh_numbers[i]}'] = val
    
    mesh_numbers = [f'mesh{i}' for i in mesh_numbers]  
    return uniform_fd_mesh_dict, mesh_numbers

# uniform_fd = make_uniform_fd(10, 15 ,5,0.1, 0.1, 100)
# print(uniform_fd[1])