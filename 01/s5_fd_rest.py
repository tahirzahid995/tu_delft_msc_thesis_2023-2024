from s0_edge_groups import data, x,y, row_df, col_df, dataset_id
import pandas as pd
import os
import time
from s2_crease_twin import dataset


print('-----------------------------------FD_REST.PY STARTS HERE--------------------------------------')

# Record the start time
start_time = time.time()


#####################################################################################################################
####################################################----INPUTS----###################################################
#####################################################################################################################

# factor for forcedensity calculation
factor = 2
exp = 1.2

#####################################################################################################################
####################################################----SOLVER----###################################################
#####################################################################################################################

# file_path = 'D:/OneDrive - Delft University of Technology/Thesis/python/00_geometry_generation/dataset/dataset.csv'
# dataset = pd.read_csv(file_path)

master_mesh_dict_3={}
master_mesh_dict_3_flat={}
# dataset = dataset['mesh_0']
for mesh in dataset.columns:
   
    dataset_mesh = dataset[mesh].tolist()

    digits = []
    list_2 = []
    list_1 = dataset_mesh
    list_2.extend([list_1[:11], list_1[11:]])

    col_row_new = []
    for c_r_i, col_row in enumerate(list_2):
        counter=0
        for i,val in enumerate(col_row):
            if val!= 1 or i==len(col_row)-1:
                count = counter
                counter = 0    
                col_row_new.append(count) 
            counter+=1 
        
        id = 0
        counter = 0
        for i,val in enumerate(col_row):
            if val==1:
                fd = round((1*((col_row_new[id])**exp/len(col_row))*factor),1)
                list_2[c_r_i][i]=fd
            
            if counter> col_row_new[id]:
                id+=1
                counter=0
            counter+=1

        digits.append(col_row_new)
        col_row_new=[]

    master_mesh_dict_3[mesh] = list_2
    master_mesh_dict_3_flat[mesh] = [i for sublist in list_2 for i in sublist]

dataset_1=pd.DataFrame(master_mesh_dict_3_flat)
# print(dataset_1[['mesh_4','mesh_88']])

# master_mesh_dict_3 = {'mesh_0': [[0.4, 0.4, 140.0, 0.4, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [0.3, 0.3, 151.0, 0.3, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]],...




#####################################################################################################################
####################################################----EXPORT----#####################################################
#####################################################################################################################

# main file path for dataset
# main_path = 'D:/OneDrive - Delft University of Technology/Thesis/python/00_geometry_generation/dataset/'

dataset_path_addition= os.path.join('DATASETS/',f"{dataset_id}/")
main_path = os.path.join(os.getcwd(), dataset_path_addition)
main_path = os.path.join(main_path,'00_geometry_generation/dataset/')

# Create the '00_geometry_generation/footprint/' folder if it does not exist
if not os.path.exists(main_path):
    os.makedirs(main_path)


# specific_path_dataset
additional_string_mesh = 'dataset_NOT1.csv'
#result path
result_path_dataset= os.path.join(main_path,additional_string_mesh)
# Export the DataFrame to a CSV file
dataset_1.to_csv(result_path_dataset, index=False)


##########################################################################################################
####################################################----END----#####################################################
#####################################################################################################################

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

print('-----------------------------------FD_REST.PY ENDS HERE--------------------------------------')