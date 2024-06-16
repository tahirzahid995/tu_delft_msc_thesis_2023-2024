import math
import numpy as np
import random
import numpy as np
import matplotlib.pyplot as plt
import time
import os
# from s0_edge_groups import dataset_id
import pandas as pd


print('-----------------------------------FD_RANDOM.PY STARTS HERE--------------------------------------')

start_time = time.time()


#####################################################################################################################
####################################################----INPUT----################################################
#####################################################################################################################

 

# user_input_iterations = int(input(f"input number of iterations"))
# user_input_iterations = 5  # Number of samples

def get_fd_random(x,y, user_input_iterations, log_min, log_max, mu, sigma):

    num_samples = ((x+1)+(y+1))*user_input_iterations

    normal_log_values  = list(np.random.normal(mu, sigma, num_samples))
    # normal_log_values = [i for i in normal_log_values if i!= 1]
    # if len(normal_log_values) < num_samples:
    #     normal_log_values.extend(np.random.choice(normal_log_values)) 
    # normal_log_values  = [abs(round(i,1)) for i in normal_log_values ]


    # Convert the logarithmic values back to their original scale
    normal_values = np.exp(normal_log_values)
    normal_values = list(np.round(normal_values,1))

    # replaces 0 with mean
    normal_values = [np.round(np.exp(mu),1) if i==0 else i for i in normal_values]

    start = 0
    j=0
    
    master_mesh_dict_3_overall = {}
    master_mesh_dict_3_overall['flat']={}
    master_mesh_dict_3_overall['not_flat']={}
    
    master_mesh_dict_3 = {}
    master_mesh_dict_3_flat = {}

    for i in range(user_input_iterations):
        mesh_id = f"mesh_{i}"
        master_mesh_dict_3[mesh_id] = []

        
        col_list = []
        while len(col_list) <= x:
            col_list.append(normal_values[j])
            j+=1

        row_list = []
        while len(row_list) <= y:
            row_list.append(normal_values[j])
            j+=1

        master_mesh_dict_3[mesh_id].append(col_list)
        master_mesh_dict_3[mesh_id].append(row_list)

        master_mesh_dict_3_flat[mesh_id] = [i for sublist in master_mesh_dict_3[mesh_id] for i in sublist]
    
    # flattened dictionary for dataset
    master_mesh_dict_3_overall['flat']= master_mesh_dict_3_flat
    # unflattened dictioanry for mesh generation in compas
    master_mesh_dict_3_overall['not_flat']= master_mesh_dict_3


    return master_mesh_dict_3_overall

#####################################################################################################################
####################################################----PLOT----#####################################################
#####################################################################################################################

# normal_values = [i for sublist in master_mesh_dict_3 for i in sublist]

# # Plot the normal distribution (in logarithmic scale)
# plt.figure(figsize=(8, 6))

# plt.hist(normal_values, bins=50, density=True, alpha=0.7, color='b')
# plt.xlabel("Log Values")
# plt.ylabel("Density")
# plt.title("Normal Distribution (Log Scale)")
# plt.grid(True)
# plt.show()



#####################################################################################################################
####################################################----TEST----#####################################################
#####################################################################################################################

# print('------normal_values--------')
# print(normal_values[:100])
# print('----------------------')
# print('------normal_log_values--------')
# print(normal_log_values[:100])
# print('----------------------')
# print('------master_mesh_dict_3--------')
# print(master_mesh_dict_3)
# print('----------------------')


#####################################################################################################################
####################################################----EXPORT----#####################################################
#####################################################################################################################
# dataset_1=pd.DataFrame(master_mesh_dict_3)


# # main file path for dataset
# # main_path = 'D:/OneDrive - Delft University of Technology/Thesis/python/00_geometry_generation/dataset/'

# dataset_path_addition= os.path.join('DATASETS/',f"{dataset_id}/")
# main_path = os.path.join(os.getcwd(), dataset_path_addition)
# main_path = os.path.join(main_path,'00_geometry_generation/dataset/')

# # Create the '00_geometry_generation/footprint/' folder if it does not exist
# if not os.path.exists(main_path):
#     os.makedirs(main_path)


# # specific_path_dataset
# additional_string_mesh = 'dataset_random.csv'
# #result path
# result_path_dataset= os.path.join(main_path,additional_string_mesh)
# # Export the DataFrame to a CSV file
# dataset_1.to_csv(result_path_dataset, index=False)

#####################################################################################################################
####################################################----END----#####################################################
#####################################################################################################################

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

print('-----------------------------------FD_RANDOM.PY ENDS HERE--------------------------------------')
