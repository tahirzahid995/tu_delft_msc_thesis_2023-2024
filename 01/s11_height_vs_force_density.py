import json
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
# import plotly.graph_objects as go
import mplcursors


print('-------------------PERFORMANCE_EVALUATION_FILTERING.PY STARTS HERE-------------------------')

# Record the start time
start_time = time.time()


#####################################################################################################################
####################################################----INPUTS----###################################################
#####################################################################################################################

datasets = ['DATASET_25']

#####################################################################################################################
####################################################----DEFINITIONS----###############################################
#####################################################################################################################


def make_mesh_dict_from_files(path, type_of_data):
    '''
    DESCRIPTION: makes a dictionary of meshes from json files of meshes
    INPUT: folder path, 
          type of data is 'pa' for performance evaluation and 'gg' for geometry generation
    OUTPUT: the dictionary of meshes with performance analysis
    '''
    # get filenames from main_path folder
    files = os.listdir(path)

    if type_of_data == 'pa':
        length = -10
    elif type_of_data == 'gg':
        length = -8
    
    # make into mesh
    mesh_data = {}
    for file_name in files:
        mesh_name = file_name[:length]
        mesh_data[mesh_name]={}
        filepath_mesh = os.path.join(path,file_name)

        with open(filepath_mesh, 'r') as file:
            mesh_data[mesh_name] = json.load(file)
    return mesh_data

def extract_keys_from_nested_dict(pa_dict, pa_keys, type_of_data):
    '''
    DESCRIPTION: Extract out the necessary performance criteria keys (Stability, Strength, Stiffness)
    INPUT: pa_dict is the performance analysis dictionary created from the definition make_mesh_dict_from_files()
    '''
    # Extract out the necessary performance criteria keys (Stability, Strength, Stiffness)
    pa_dict_sss = {mesh: {key: pa_dict[mesh][key] for key in pa_keys} for mesh in pa_dict}
    

    # Check whether there is failure in Stability or Strength (Stiffness check is already done)
    if type_of_data == 'pa':  
        for mesh in pa_dict_sss:
            if pa_dict_sss[mesh]['Buckling_Load_Factor'] > 1 : 
                pa_dict_sss[mesh]['Buckling_Load_Factor_Failure'] = 'False'
            else:
                pa_dict_sss[mesh]['Buckling_Load_Factor_Failure'] = 'True'

            if pa_dict_sss[mesh]['Utilization'] < 1 : 
                pa_dict_sss[mesh]['Utilization_Failure'] = 'False'
            else:
                pa_dict_sss[mesh]['Utilization_Failure'] = 'True'
    
    return pa_dict_sss

#####################################################################################################################
####################################################----SOLVER----###############################################
#####################################################################################################################

# main path
# main_path = 'D:/OneDrive - Delft University of Technology/Thesis/python/DATASETS/'
main_path = os.path.join(os.getcwd(),'DATASETS/')

main_path_dict= {}
main_path_dict['pa']={}
main_path_dict['gg']={}
for i, val in enumerate(datasets):
    main_path_dict['pa'][val]= os.path.join(main_path,val,'01_performance_evaluation/dataset_separate/' )
    main_path_dict['gg'][val]= os.path.join(main_path,val,'00_geometry_generation/dataset_separate/dataset_separate_height_thickness/' )
    

# keys for SSS
keys_sss  = ['Buckling_Load_Factor','Utilization','Interstorey_Drift_Ratios', 'Interstorey_Drift_Failure']
# keys for pinned support vs fixed support comparison
keys_ss = ['Buckling_Load_Factor','Utilization', 'Max_Displacement/mm']
# key for height
key_height = ['Height_of_vault/m'] 


################## json to dictionary + extracting only SSS keys


pa_dict = {}
gg_height_dict = {}
for dataset, path in main_path_dict['pa'].items():
    pa_dict[dataset] = make_mesh_dict_from_files(path, 'pa')
    pa_dict[dataset] = extract_keys_from_nested_dict(pa_dict[dataset], keys_ss, 'pa')
    pa_dict[dataset] = pd.DataFrame.from_dict(pa_dict[dataset])

for dataset, path in main_path_dict['gg'].items():
    gg_height_dict[dataset] = make_mesh_dict_from_files(path, 'gg')
    gg_height_dict[dataset] = extract_keys_from_nested_dict(gg_height_dict[dataset], key_height, 'gg')
    gg_height_dict[dataset] = pd.DataFrame.from_dict(gg_height_dict[dataset])


# Convert nested dictionary to DataFrame
gg_height_df = pd.DataFrame.from_dict(gg_height_dict[dataset])

# Sort column names in ascending order considering numerical part
sorted_columns_height = sorted(gg_height_df.columns, key=lambda x: int(x.split('mesh_')[-1]))
# Reorder DataFrame columns
gg_height_df_sorted = gg_height_df[sorted_columns_height]

gg_height_dict_sorted = gg_height_df_sorted.to_dict(orient='records')[0]


################## extracting uniform force densties for each mesh

dataset_file_path = os.path.join(main_path, datasets[0], '00_geometry_generation\dataset\dataset.csv')
df = pd.read_csv(dataset_file_path)

fd_dict = {}
for mesh in df.columns:
    fd_dict[mesh] = df[mesh].iloc[0]

#####################################################################################################################
####################################################----PLOT----#####################################################
#####################################################################################################################

plot_location = os.path.join(main_path,f'plots/height_vs_fd/{datasets[0]}')
if not os.path.exists(plot_location):
    os.makedirs(plot_location)


plotting_dict_height_fd = {}
for mesh in fd_dict.keys():
    plotting_dict_height_fd[mesh] = {}
    plotting_dict_height_fd[mesh]['height']= gg_height_dict_sorted[mesh]
    plotting_dict_height_fd[mesh]['fd']= fd_dict[mesh]

print(plotting_dict_height_fd)

############################################################################## HOVER GRAPH USING MPLCURSORS

# # Define colors for each dataset
# colors = ['blue', 'red']
# Define custom color
colour_dark_blue = (11/255, 58/255, 64/255)  # Normalize RGB values to range [0, 1]
colour_teal = (15/255, 117/255, 118/255)  # Normalize RGB values to range [0, 1]
colour_maroon = (170/255, 80/255, 38/255)  # Normalize RGB values to range [0, 1]
colour_gold = (190/255, 181/255, 111/255)  # Normalize RGB values to range [0, 1]
colour_orange= (241/255, 118/255, 34/255)  # Normalize RGB values to range [0, 1]

colour_list = [colour_teal, colour_orange, colour_maroon]
# Define colors for each dataset
colors = [colour_orange ,colour_teal]

##################################################### HEGIHT VS UTILIZATION

# Extract heights and fds from the data
heights = [info['height'] for info in plotting_dict_height_fd.values()]
fds = [info['fd'] for info in plotting_dict_height_fd.values()]

# Plot the graph
plt.plot(fds, heights, 'o', color = colour_teal)  # 'o' for scatter plot
plt.xlabel('Force Density')
plt.ylabel('Height/m')
plt.title('HEIGHT VS FORCE_DENSITY')
plt.grid(True)
plt.savefig(os.path.join(plot_location, f'plot_height_vs_fd.png'), dpi=300)
plt.show()




#####################################################################################################################
####################################################----TESTING----##################################################
#####################################################################################################################


# print('----------------------------')
# print('MESHES')
# print(list(pa_supports_fixed.keys()))
# print('----------------------------')
# print('df_pa_supports_fixed')
# print(df_pa_supports_fixed_ss)
# print('----------------------------')
# print('df_pa_supports_pinned')
# print(df_pa_supports_pinned_ss)
# print('----------------------------')
# print('df_index')
# print(list(df_pa_supports_pinned_ss.loc['Buckling_Load_Factor']))

#####################################################################################################################
####################################################----END----######################################################
#####################################################################################################################

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

print('------------------------PERFORMANCE_EVALUATION_FILTERING.PY ENDS HERE--------------------------------------')