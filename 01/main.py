import numpy
import time
from pprint import pprint
import json
import csv
import os
from s0_edge_groups import *
from s7_fd_random import get_fd_random
from s6_my_compas_fd_rest_diff import get_compas_meshes
import math
import pandas as pd
from s10_unifom_force_density_meshes import make_uniform_fd


print('-----------------------------------EDGE GROUPS.PY STARTS HERE--------------------------------------')

# Record the start time
start_time = time.time()


#####################################################################################################################
####################################################----INPUTS----###################################################
#####################################################################################################################

y = 15
x= 10
#number of divisions 
x_div =  x
y_div = y
# size of footprint in metres
x_size = x
y_size = y

dataset_id = 'DATASET_28'

load_all = 40.0

user_input_iterations = int(input(f"input number of iterations"))

# include uniform force densities
BOOLEAN_uniform_fd = True
max_uniform_fd = 5.0
min_uniform_fd = 0.1                        
increments_uniform_fd = 0.1                 # increment of increase
uniform_fd_positioning = 'random'      # 'consecutive' or 'random'



#####################################################################################################################
#######################----GENERATE NEW COMPAS MESHES FOR DIFFFERENT LOAD FROM EXISTING DATASET----##################
#####################################################################################################################

# Set boolean. 
BOOLEAN_predefined_dataset = True
# location of dataset
# predefined_dataset_file_path = os.path.join(os.getcwd(),'DATASETS/DATASET_13/00_geometry_generation/dataset/dataset.csv')
predefined_dataset_file_path = os.path.join(os.getcwd(),'DATASETS/')
predefined_dataset_file_path = os.path.join(predefined_dataset_file_path,f"{dataset_id}/")
predefined_dataset_file_path = os.path.join(predefined_dataset_file_path,'00_geometry_generation/dataset/dataset.csv')


# Generate a dataset of new force densities from scratch or generate from an existing csv with pred-defined force-densities  
if BOOLEAN_predefined_dataset == True:

    df = pd.read_csv(predefined_dataset_file_path)

    df_dict = df.to_dict('list')

    # Number of keys to extract
    n = user_input_iterations
    # Extract the first n keys
    df_dict = {key: df_dict[key] for key in list(df_dict.keys())[:n]}

    for mesh, fd in df_dict.items():
        col = df_dict[mesh][:x+1]
        row = df_dict[mesh][x+1:]
        df_dict[mesh]= [col]
        df_dict[mesh].append(row)
    
    dataset_for_compas = df_dict
    dataset_for_vae = df



####################################################----S0_EDGE_GROUPS----############################################

'''GETTING THE POLYEDGES'''

polyedge_dictionary = get_polyedges(x,y)
row_df = polyedge_dictionary['row_df']
col_df = polyedge_dictionary['col_df']


####################################################----S7_FD_RANDOM----############################################

'''GETTING THE DICTIONARY OF MESHES WITH RANDOMIZED FORCE DENSITIES NORMALLY DISTRIBUTED IN A LOGARITHIMIC SCALE'''

if BOOLEAN_predefined_dataset == False:
    log_min = math.log(0.2) #log10(0.2)
    log_max = math.log(100) #log10(10000)
    mu = math.log(1)  # Mean
    sigma = (log_max - log_min) /4 # Standard deviation  (log_max - log_min) /3

    master_mesh_final= get_fd_random(x,y, user_input_iterations, log_min, log_max, mu, sigma)

    # for compas mesh generation
    dataset_for_compas = master_mesh_final['not_flat']

    # for vae
    dataset_for_vae = pd.DataFrame(master_mesh_final['flat'])


    if BOOLEAN_uniform_fd == True:
        ################## uniform force densities for compas
        uniform_fd, uniform_mesh_ids = make_uniform_fd(x,y,max_uniform_fd, min_uniform_fd, increments_uniform_fd, user_input_iterations, uniform_fd_positioning)

        ################## uniform force densities for vae
        uniform_fd_flat = {}
        for mesh in uniform_fd.keys():
            uniform_fd_flat[mesh]=[i for sublist in uniform_fd[mesh] for i in sublist]
        df_uniform = pd.DataFrame(uniform_fd_flat)

        ################## replacing the uniform meshes in the main dataset

        for mesh in df_uniform.columns:
            dataset_for_vae[mesh] = df_uniform[mesh]
            dataset_for_compas[mesh] = uniform_fd[mesh]


#######################################----S6_MY_COMPAS_FD_REST_DIFF----################################

'''GETTING THE COMPAS MESHES'''

master_mesh_compas = get_compas_meshes(x_size, y_size, x_div, y_div, dataset_for_compas, load_all, col_df, row_df)

master_mesh_compas_edges = master_mesh_compas['edges']
master_mesh_compas_meshes = master_mesh_compas['meshes']


#####################################################################################################################
####################################################----EXPORT----#####################################################
#####################################################################################################################

# MAIN PATH
main_path_addition= os.path.join('DATASETS/',f"{dataset_id}/")
main_path = os.path.join(os.getcwd(), main_path_addition)


#############################################################################    POLYEDGES (s0_edge_groups)

footprint_path = os.path.join(main_path,'00_geometry_generation/footprint/')
# Create the '00_geometry_generation/footprint/' folder if it does not exist
if not os.path.exists(footprint_path):
    os.makedirs(footprint_path)

# specific_path_rows
additional_string_row = f"x={x},y={y}_row_dict.csv"
#result path_rows
result_path_row = os.path.join(footprint_path,additional_string_row)

# specific_path_col
additional_string_col = f"x={x},y={y}_col_dict.csv"
#result path_col
result_path_col = os.path.join(footprint_path,additional_string_col)

# Export the DataFrame to a CSV file
row_df.to_csv(result_path_row, index=False)
col_df.to_csv(result_path_col, index=False)



#############################################################################    FD_DATASET (s7_fd_random)

dataset_path_addition= os.path.join('DATASETS/',f"{dataset_id}/")
dataset_path = os.path.join(os.getcwd(), dataset_path_addition)
dataset_path = os.path.join(dataset_path,'00_geometry_generation/dataset/')

# Create the '00_geometry_generation/dataset/' folder if it does not exist
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# specific_path_dataset
additional_string_mesh = 'dataset.csv'
#result path
result_path_dataset= os.path.join(dataset_path,additional_string_mesh)
# Export the DataFrame to a CSV file
dataset_for_vae.to_csv(result_path_dataset, index=False)


if BOOLEAN_predefined_dataset == False:
    # specific_path_uniform_mesh_ids
    additional_string_mesh_uniform = 'uniform_mesh_ids.txt'
    #result path
    result_path_mesh_uniform= os.path.join(dataset_path,additional_string_mesh_uniform)

    # Open a file in write mode ('w')
    with open(result_path_mesh_uniform, "w") as output:
        output.write(str(uniform_mesh_ids))

#############################################################################    COMPAS MESHES (s6_my_compas_fd_rest_diff)

# mesh path
mesh_path = os.path.join(main_path,'00_geometry_generation/mesh/')
# Create the '00_geometry_generation/mesh/' folder if it does not exist
if not os.path.exists(mesh_path):
    os.makedirs(mesh_path)


for mesh_local,mesh in master_mesh_compas_meshes.items():
    # specific_path_mesh
    additional_string_mesh = f"{mesh_local}.json"
    result_path_mesh = os.path.join(mesh_path,additional_string_mesh)
    #result path
    mesh.to_json(result_path_mesh)

    # specific_path_edges
    additional_string_edges = f"{mesh_local}_edges.json"
    #result path
    result_path_edges= os.path.join(mesh_path,additional_string_edges)
    with open(result_path_edges, 'w') as json_file:
        json.dump(master_mesh_compas_edges,json_file, indent = 1)



# # Plot the normal distribution (in logarithmic scale)
# plt.figure(figsize=(8, 6))

# plt.hist(normal_values, bins=50, density=True, alpha=0.7, color='b')
# plt.xlabel("Log Values")
# plt.ylabel("Density")
# plt.title("Normal Distribution (Log Scale)")
# plt.grid(True)
# plt.show()
