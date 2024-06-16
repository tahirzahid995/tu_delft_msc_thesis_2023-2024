import copy
from s1_crease_calculator import combination_col_list_symm, combination_col_list_symm_not, combination_row_list_symm, combination_row_list_symm_not, row_list_symm, col_list_symm, col_list, row_list
from s0_edge_groups import row_df, col_df,dataset_id
import time
import random
import json
import pandas as pd
import os
import copy
import numpy as np

print('-----------------------------------CREASE TWIN.PY STARTS HERE--------------------------------------')

start_time = time.time()

#####################################################################################################################
####################################################----DEFINITION----################################################
#####################################################################################################################


def are_meshes_identical(mesh1, mesh2):
    return set(mesh1) == set(mesh2)

def get_twins(meshes):
    '''
    DESCRIPTION:
    Matches keys with the same values regardless of the order of the values.

    example:

    INPUT:
    r_ = {'r_1': [1, 2, 3], 'r_2': [1, 2], 'r_3': [5], 'r_4': [3, 2, 1], 'r_5': [2, 1], 'r_6': [1]}

    OUTPUT:
    [['r_2', 'r_5'], ['r_1', 'r_4']]
    '''

    # Check for identical meshes
    twins =[]
    twins_not = []
    for mesh1_name, mesh1_values in meshes.items():
        for mesh2_name, mesh2_values in meshes.items():
            if mesh1_name != mesh2_name and are_meshes_identical(mesh1_values, mesh2_values):
                twins.append([mesh1_name, mesh2_name])

    # Remove duplicate twins

    # Convert each inner list to a set and then use a set to eliminate duplicates
    unique_twins = list(map(lambda x: sorted(set(x)), twins))
    # Remove duplicate lists
    unique_twins = list(set(map(tuple, unique_twins)))
    # Convert back to a list of lists
    unique_twins = [list(item) for item in unique_twins]

    return unique_twins

def remove_smaller_lists(lists):
    '''
    DESCRIPTION:
    Checks if whether there an item is found in more than list inside a nested list. Then deletes the smaller list.

    INPUT: [[1,4],[1,2,3,4],[5,6]]

    OUTPUT: [[1,2,3,4],[5,6]]
    '''
    result = []
    for i, current_list in enumerate(lists):
        is_smaller_list = any(len(current_list) < len(other_list) and any(value in other_list for value in current_list) for other_list in lists[:i] + lists[i+1:])
        if not is_smaller_list:
            result.append(current_list)
    return result

def symmetry_finding(x,a,z):
    '''
    DESCRIPTION:
    Finds symmetrical row/column combinations. For example: 'r_1':[1,2,3] and 'r_4':[11,12,13] may be symmetrical
    so both would produce the same geometry. This allows us to identify which combinations are symmetrical.

    INPUTS:
    x = [1,2,3,4,5,6,7,8,9,10,11,12,13]. It is the list of rows/columns present
    a = {'r_1':[1,2,3],'r_2':[1,2],'r_3':[5]}. It is the dictionary of non-symmetrical row/column combinations
    z = {'r_4':[11,12,13],'r_5':[12,13],'r_6':[13]}. It is the dictionary of symmetrical row/column combinations (i.e they are repetitions of the non-symmetrical combinations)
    

    OUTPUTS:
    b = {'r_1': [1, 2, 3], 'r_2': [1, 2], 'r_3': [5], 'r_4': [3, 2, 1], 'r_5': [2, 1], 'r_6': [1]}.
    The row/column numbers of the symmetrical_combinations have been flipped to their symmetrical counterparts so they
    can be processed later. Note the difference of r_4, r_5, and r_6 in z and in b.
    '''


    # making dictionary that flips the symmetrical numbers
    dict_flip = {}
    for i,val in enumerate(x):
        j = -1*(i+1)
        dict_flip[val]= x[j]
    #ouptut-------------dict_flip = {1: 13, 2: 12, 3: 11, 4: 10, 5: 9, 6: 8, 7: 7, 8: 6, 9: 5, 10: 4, 11: 3, 12: 2, 13: 1}


    # flipping the symmetrical numbers. [11,12,13] becomes [3,2,1]
    z_flip = copy.deepcopy(z)
    for key in z.keys():
        for i, val in enumerate(z[key]):
            z_flip[key][i] = dict_flip[val]
    #ouptut------------------z = {'r_4': [11, 12, 13], 'r_5': [12, 13], 'r_6': [13]}
    #-------------------z_flip = {'r_4': [3, 2, 1], 'r_5': [2, 1], 'r_6': [1]}


    # combines the symmetrical and non_symmetrical combinations into one dictionary
    b=copy.deepcopy(a)
    for key,val in z_flip.items():
        b[key] = val
    #ouptut------------------b = {'r_1': [1, 2, 3], 'r_2': [1, 2], 'r_3': [5], 'r_4': [3, 2, 1], 'r_5': [2, 1], 'r_6': [1]}

    return b


#####################################################################################################################
####################################################----INPUTS----################################################
#####################################################################################################################

# generating samples for force_densities 
mu = 150  # Mean
sigma = 30  # Standard deviation
num_samples = 1000  # Number of samples

fd_crease_list  = list(np.random.normal(mu, sigma, num_samples))
fd_crease_list  = [round(i,0) for i in fd_crease_list ]


user_input_iterations = int(input(f"input number of iterations"))
fd_rest_list = [1.0]





#####################################################################################################################
####################################################----SOLVER----################################################
#####################################################################################################################


#################################################### Making dictionary from column/row combinations

# print(combination_col_list_symm_not)
comb_dict = {}
comb_dict['col_symm'] = {}
comb_dict['col_symm_not'] = {}
comb_dict['row_symm'] = {}
comb_dict['row_symm_not'] = {}


# columns
i=0
for val in combination_col_list_symm_not:
    comb_dict['col_symm_not'][f"c_{i}"] = val
    i+=1


for val in combination_col_list_symm:
    comb_dict['col_symm'][f"c_{i}"]  = val
    i+=1

# rows    
i=0
for val in combination_row_list_symm_not:
    comb_dict['row_symm_not'][f"r_{i}"]  = val
    i+=1
    
for val in combination_row_list_symm:
    comb_dict['row_symm'][f"r_{i}"]  = val
    i+=1

# flattening the combinations into a single dictionary
comb_dict_flat = {}
for key in comb_dict.keys():
    for combination, val in comb_dict[key].items():
        comb_dict_flat[combination] = comb_dict[key][combination]

#ouptut------------------comb_dict = {'row_symm': {'r_0': [2], 'r_1': [3], 'r_2': [4], 'r_3': [5], 'r_4': [2, 5], 'r_5': [2, 6]...}
#ouptut-------------comb_dict_flat = {'c_69': [3, 5, 7, 10], 'c_74': [4, 6, 8, 10], 'c_75': [2, 4, 6, 8, 10], ' 'r_364': [8, 13], 'r_365': [9, 12], 'r_366': [9, 13], 'r_367': [10, 13], 'r_368': [8, 10]...}


# dictionary where indices of columns and rows combinations have been exchanged with that of twin.
# r_list is the list of combination of rows, c_list is the list of combination of columns
c_list = symmetry_finding(col_list, comb_dict['col_symm_not'], comb_dict['col_symm'])
r_list = symmetry_finding(row_list, comb_dict['row_symm_not'], comb_dict['row_symm'])

# r_list = {'r_1': [1, 2, 3], 'r_2': [1, 2], 'r_3': [5], 'r_4': [3, 2, 1], 'r_5': [2, 1], 'r_6': [1]}
# c_list = {'c_1': [1, 2, 3], 'c_2': [1, 2], 'c_3': [5], 'c_4': [3, 2, 1], 'c_5': [2, 1], 'c_6': [1]}


# making mesh dictionary
i = 0
iterations = 1
mesh_dict = {}
break_flag = False
for r_ in r_list.keys():
    for c_ in c_list.keys():
        mesh_dict[f"mesh_{i}"] = [c_, r_]
        i+=1
        iterations += 1
        if iterations > user_input_iterations:
            break_flag = True
            break
    if break_flag:
        break
#ouptut------------------mesh_dict = {'mesh_0': ['c_1', 'r_1'], 'mesh_1': ['c_2', 'r_1']...}



#################################################### GETTING TWINS
twins={}
twins['col'] = get_twins(c_list)
twins['row'] = get_twins(r_list)

# dictionary where one twin (column/row combination) is the key and the other is the value
twins['dict'] = {}
for key in twins:
    if key == 'dict':
        break
    for pair in twins[key]:
        twins['dict'][pair[0]] =  pair[1]
#ouptut-----------------------twins['dict'] = {'c_2': 'c_5', 'c_1': 'c_4', 'r_1': 'r_4', 'r_2': 'r_5'}

# flattened list of twins 
# twin_flat_col = [item for sublist in twins['col'] for item in sublist]
# twin_flat_row = [item for sublist in twins['row'] for item in sublist]
# twins['flat'] = {}
# twins['flat'] = twin_flat_col
# twins['flat'].extend(twin_flat_row)
# twins['flat_half'] = [twins['flat'][i] for i in range(0, len(twins['flat']),2)]


# replaces row/column combination of standardized twin. eg c_1 and c_4 are twins. all c_1s are replaced by c_4.
mesh_dict_copy = copy.deepcopy(mesh_dict)
for mesh, combination in mesh_dict.items():
    for i, val in enumerate(mesh_dict[mesh]):
        if val in twins['dict'].keys():
            mesh_dict_copy[mesh][i] = twins['dict'][val]
#ouptut-----------------------mesh_dict = {'mesh_0': ['c_1', 'r_1'], 'mesh_1': ['c_2', 'r_1'], 'mesh_2': ['c_3', 'r_1'], 'mesh_3': ['c_4', 'r_1'], 'mesh_4': ['c_5', 'r_1']..}
#ouptut------------------mesh_dict_copy = {'mesh_0': ['c_4', 'r_4'], 'mesh_1': ['c_5', 'r_4'], 'mesh_2': ['c_3', 'r_4'], 'mesh_3': ['c_4', 'r_4'], 'mesh_4': ['c_5', 'r_4']..}


# Nested list of all mesh twins (unrefined)
mesh_lists_twins = get_twins(mesh_dict_copy)            
#ouptut------------------mesh_lists = [['mesh_24', 'mesh_6'], ['mesh_1', 'mesh_22'] , ['mesh_1', 'mesh_22']...]       

# list of all mesh
mesh_lists = []
for mesh in mesh_dict_copy.keys():
    mesh_lists.append(mesh)
#ouptut------------------mesh_lists = ['mesh_0', 'mesh_1', 'mesh_2', 'mesh_3', 'mesh_4', 'mesh_5', 'mesh_6', 'mesh_7', 'mesh_8...]


# Merging lists with repeating elements so quadruplets are grouped. [[1,2],[1,3]] will merge into [[1,2,3],[1,3]]
merged_mesh_lists = []

for sublist in mesh_lists_twins:
    merged = False

    for existing_list in merged_mesh_lists:
        if any(item in existing_list for item in sublist):
            existing_list.extend(item for item in sublist if item not in existing_list)
            merged = True
            break

    if not merged:
        merged_mesh_lists.append(sublist)


# Removing smaller lists with repeating elements. [[1,2,3],[1,3]] will filter into [[1,2,3]]
merged_mesh_lists = remove_smaller_lists(merged_mesh_lists)

# Remove duplicates from the merged lists
merged_mesh_lists = [list(set(sublist)) for sublist in merged_mesh_lists]
# print(merged_mesh_lists)

# Flattening and sorting merged lists to check if all items are present from original meshed list
merged_mesh_lists_flat = [item for sublist in merged_mesh_lists for item in (sublist if isinstance(sublist, list) else [sublist])]
merged_mesh_lists_flat = sorted(merged_mesh_lists_flat, key=lambda x: int(x.split('_')[1]))


# check for meshes with no twins 
twins_not = []
for mesh in mesh_lists:
    if mesh not in merged_mesh_lists_flat:
        twins_not.append(mesh)
#ouptut------------------twins_not = ['mesh_14', 'mesh_17', 'mesh_32', 'mesh_35']


# Extending the list of meshes to include those that do not have twins
twins_not = [[i] for i in twins_not] 
merged_mesh_lists.extend(twins_not)


# Check for missing meshes after merging list without twins 
merged_mesh_lists_flat.extend(twins_not)
missing_mesh = []
for value_to_check in mesh_dict.keys():

    is_present = any(value_to_check in sublist for sublist in merged_mesh_lists_flat)
    if is_present == False:
        missing_mesh.append(value_to_check)

if len(missing_mesh) > 0:
    print(f"Missing meshes: {missing_mesh}")
else:
    print(f"No Missing meshes")



#################################################### GETTING MASTER MESH DICTIONARY

'''
This contains the following:
a) mesh_0           --- mesh number
b) c_20 / r_35      --- row/column combination 
c) [2,9,10,11]     --- list of rows or columns in those row/column combinations 
'''

master_mesh_dict = {}
for mesh in mesh_dict.keys():

    # if Option 1
    # master_mesh_dict[mesh] = {}

    # if Option 2
    master_mesh_dict[mesh] = []

    for rc_comb in mesh_dict[mesh]:

        # Option 1: adds r_12,c_35 as well
        # master_mesh_dict[mesh][rc_comb] = comb_dict_flat[rc_comb]

        # Option 2: does not add r_12,c_35 
        master_mesh_dict[mesh].append(comb_dict_flat[rc_comb])  

#ouptut--------Option 1----------master_mesh_dict = {'mesh_14': [[3, 10], [2]], 'mesh_15': [[4, 7], [2]], 'mesh_16': [[4, 8], [2]]}
#ouptut--------Option 2----------master_mesh_dict = {'mesh_14': {'c_14': [3, 10], 'r_0': [2]}, 'mesh_15': {'c_15': [4, 7], 'r_0': [2]}, 'mesh_16': {'c_16': [4, 8], 'r_0': [2]}}

#####################################################################################################################
####################################################----FIND MESHES----##############################################
#####################################################################################################################

########################################### To find twins of a given mesh 
mesh_to_find = 'mesh_1'
for i,combination in enumerate(merged_mesh_lists):
    if mesh_to_find in combination:
        print(f"Combination twins are {combination}")

# ########################################### To find meshes with a given number of twins
# # number of twins required. 0 means no twins.
# number_of_twins = 0

# req_meshes = []
# for combination in merged_mesh_lists:
#     if len(combination) == number_of_twins + 1:
#         req_meshes.append(combination)
# print(req_meshes)


#####################################################################################################################
####################################################----FIND EDEGS----##############################################
#####################################################################################################################


# # retrieving the first n meshes just for testing
# master_mesh_dict = dict(list(master_mesh_dict.items())[:2])
        
# definition for retrieving the first mesh just for testing
def get_first_item(original_dict):
    # Check if the original dictionary is not empty
    if original_dict:
        # Use next() to get the first key-value pair and create a new dictionary
        first_item = {next(iter(original_dict)): original_dict[next(iter(original_dict))]}
        return first_item
    else:
        # If the original dictionary is empty, return an empty dictionary
        return {}
 
# definiton for retrieving any one mesh just for testing    
def get_item_by_key(original_dict, target_key):
    # Check if the key exists in the original dictionary
    if target_key in original_dict:
        # Create a new dictionary with the specified key-value pair
        selected_item = {target_key: original_dict[target_key]}
        return selected_item
    else:
        # If the key does not exist, return an empty dictionary
        return {}


# # retrieving any one random mesh just for testing
# random_number = random.randint(1,len(master_mesh_dict.keys()))
# sel_mesh = f"mesh_{random_number}"

# # retrieving any one mesh just for testing
# sel_mesh = 'mesh_74'
# master_mesh_dict = get_item_by_key(master_mesh_dict, sel_mesh)




########## final dataset structure 
p_edge_all = list(col_df)
p_edge_all.extend(list(row_df))
#ouptut------------------p_edge_all = ['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6', 'col_7', 'col_8', 'col_9', 'col_10', 'col_11', 'row_1', 'row_2', 'row_3', 'row_4', 'row_5', 'row_6', 'row_7', 'row_8', 'row_9', 'row_10', 'row_11', 'row_12', 'row_13', 'row_14']

p_edge_all_dict = {}
for i,val in enumerate(p_edge_all):
    p_edge_all_dict[val] = i
#ouptut------------------p_edge_all_dict = {'col_1': 0, 'col_2': 1, 'col_3': 2, 'col_4': 3, 'col_5': 4, 'col_6': 5, 'col_7': 6, 'col_8': 7, 'col_9': 8, 'col_10': 9, 'col_11': 10, 'row_1': 11, 'row_2': 12, 'row_3': 13, 'row_4': 14, 'row_5': 15, 'row_6': 16, 'row_7': 17, 'row_8': 18, 'row_9': 19, 'row_10': 20, 'row_11': 21, 'row_12': 22, 'row_13': 23, 'row_14': 24}      



# # master_mesh_dict_2={}
# for mesh in master_mesh_dict.keys():
#     # p_edge_all_fd = []
#     # while len(p_edge_all_fd) <= len(p_edge_all):
#     #     p_edge_all_fd.append(master_mesh_dict_1[mesh]['fd_rest'])
    
#     # p_edge_all_fd = copy.deepcopy(p_edge_all) 

#     # columns
#     for i, c_r in enumerate(master_mesh_dict[mesh][0]):  
#         id = f"col_{c_r}"
#         master_mesh_dict_1[mesh]['col'].keys()
#         p_edge_all_fd[p_edge_all_dict[id]] = list(master_mesh_dict_1[mesh]['col'].keys())[i]
#         master_mesh_dict_2[mesh] = p_edge_all_fd


master_mesh_dict_1 = {}
master_mesh_dict_2={}

for mesh in master_mesh_dict.keys():
        #master_mesh_dict_2
        p_edge_all_fd = copy.deepcopy(p_edge_all)
        #master_mesh_dict_1
        fd_rest = random.choice(fd_rest_list)
        master_mesh_dict_1[mesh] = {}
        master_mesh_dict_1[mesh]['fd_rest'] = fd_rest
        master_mesh_dict_1[mesh]['col'] = {}
        master_mesh_dict_1[mesh]['row'] = {}
        # edges_col = []
        # edges_row = []

        for i, c_r_comb in enumerate(master_mesh_dict[mesh]):
            if len(master_mesh_dict[mesh])==2:
                fd_list_col = []
                fd_list_row = []
                for c_r in master_mesh_dict[mesh][i]:
                 
                    # columns
                    if i == 0:
                        edges= list(col_df[f"col_{c_r}"])
                        # edges_col.extend(edges)
                        fd_crease = random.choice(fd_crease_list)
                        
                        if fd_crease not in fd_list_col:
                            master_mesh_dict_1[mesh]['col'][f"fd_{fd_crease}"]= edges
                        else:
                            master_mesh_dict_1[mesh]['col'][f"fd_{fd_crease}"].extend(edges)

                        fd_list_col.append(fd_crease)

                        ############ master_mesh_dict_2 fd_columns
                        id = f"col_{c_r}"
                        p_edge_all_fd[p_edge_all_dict[id]] = fd_crease
                        master_mesh_dict_2[mesh] = p_edge_all_fd

                    # rows 
                    else:
                        edges= list(row_df[f"row_{c_r}"])
                        # edges_row.append(edges)
                        fd_crease = random.choice(fd_crease_list)

                        if fd_crease not in fd_list_row:
                            master_mesh_dict_1[mesh]['row'][f"fd_{fd_crease}"]= edges
                        else:
                            master_mesh_dict_1[mesh]['row'][f"fd_{fd_crease}"].extend(edges)

                        fd_list_row.append(fd_crease)

                        ############ master_mesh_dict_2 fd_rows
                        id = f"row_{c_r}"
                        p_edge_all_fd[p_edge_all_dict[id]] = fd_crease
                        master_mesh_dict_2[mesh] = p_edge_all_fd

                    ############ master_mesh_dict_2 fd_rest
                    p_edge_all_fd = [item if not isinstance(item, str) else fd_rest for item in p_edge_all_fd]
                    master_mesh_dict_2[mesh] = p_edge_all_fd

                        # master_mesh_dict_1[mesh]['row'][f"fd_{fd_crease}"] = edges  
                # master_mesh_dict_1[mesh]['col'] = edges_col
                # master_mesh_dict_1[mesh]['row'] = edges_row 
                    
# {'mesh_0': [1.0, 1.0, 120.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 158.0, 1.0, 1.0, 1.0, 1.0, 1.0, ...], 'mesh_1': [1.0, 1.0, 1.0, 145.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 174.0, 1.0, 1.0, 1.0, 1.0, 1.0, ...]}
# {'mesh_45': {'fd_rest': 50.0, 'col': {'fd_150': [216, 218, 220, 222, 224, 227, 228, 230, 232, 234, 236, 238, 241], 'fd_50': [108, 110, 112, 114, 116, 119, 120, 122, 124, 126, 128, 130, 133]}, 'row': {'fd_100': [2, 30, 57, 84, 111, 138, 165, 192, 219, 246]}}}
#####################################################################################################################
####################################################----TEST----#####################################################
#####################################################################################################################


# print('-----------------------------------')
# print("----------Master mesh dict--------------------")
# print(master_mesh_dict['mesh_74'])
# print('-----------------------------------')
# print('--------twins_not------------')
# print(len(twins_not))   
# print('----------------------')
# print('------merged_mesh_lists_flat--------')
# print(len(merged_mesh_lists_flat))
# print('----------------------')
# print('------mesh--------')
# print([merged_mesh_lists_flat[50]])
# print('-----------------------------------')
# print('--------comb_dict------------')
# print(comb_dict)   
# print('-----------------------------------')
# print('--------Master mesh dict_1------------')
# print(master_mesh_dict_1['mesh_74'])
# print('-----------------------------------')
# print('--------col_df------------')
# print(col_df)
# print('-----------------------------------')

#####################################################################################################################
####################################################----CONVERT----#####################################################
#####################################################################################################################

dataset = pd.DataFrame(master_mesh_dict_2)

#####################################################################################################################
####################################################----EXPORT----#####################################################
#####################################################################################################################



# # main file path
# main_path = 'D:/OneDrive - Delft University of Technology/Thesis/python/00_geometry_generation/mesh/'
dataset_path_addition= os.path.join('DATASETS/',f"{dataset_id}/")
main_path = os.path.join(os.getcwd(), dataset_path_addition)
main_path = os.path.join(main_path,'00_geometry_generation/')




mesh_path = os.path.join(main_path,'mesh/') 
# Create the '00_geometry_generation/mesh/' folder if it does not exist
if not os.path.exists(mesh_path):
    os.makedirs(mesh_path)

# specific_path_master_mesh_dict
additional_string_mesh = 'master_mesh_dict.json'
# result path
result_path_master_mesh = os.path.join(mesh_path,additional_string_mesh)
# Export json
with open(result_path_master_mesh, 'w') as json_file:
    json.dump(master_mesh_dict,json_file, indent = 1)


# specific_path_master_mesh_dict_1
additional_string_mesh = 'master_mesh_dict_1.json'
# result path
result_path_master_mesh_1 = os.path.join(mesh_path,additional_string_mesh)
# Export json
with open(result_path_master_mesh_1, 'w') as json_file:
    json.dump(master_mesh_dict_1,json_file, indent = 1)




# main file path for dataset
# main_path = 'D:/OneDrive - Delft University of Technology/Thesis/python/00_geometry_generation/dataset/'
dataset_path = os.path.join(main_path,'dataset/')     
# Create the '00_geometry_generation/dataset/' folder if it does not exist
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# specific_path_dataset
additional_string_mesh = 'dataset.csv'
#result path
result_path_dataset= os.path.join(dataset_path,additional_string_mesh)
# Export the DataFrame to a CSV file
dataset.to_csv(result_path_dataset, index=False)


# mesh_selected = master_mesh_dict_1['mesh_90']
# columns = [val for i, val in master_mesh_dict_1['mesh_90']['col'].items()]
# columns = [i for i in sublist for sublist in columns]
# print(f"items are {columns}")
# print(f"columns = {master_mesh_dict_1['mesh_90']['col']}")
# print(f"rows = {master_mesh_dict_1['mesh_90']['row']}")

#####################################################################################################################
####################################################----END----#####################################################
#####################################################################################################################

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

print('-----------------------------------CREASE TWIN.PY ENDS HERE--------------------------------------')
