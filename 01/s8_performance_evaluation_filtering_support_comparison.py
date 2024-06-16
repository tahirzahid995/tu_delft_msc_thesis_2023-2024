import json
import pandas as pd
import os
import time
import matplotlib.pyplot as plt


print('-------------------PERFORMANCE_EVALUATION_FILTERING.PY STARTS HERE-------------------------')

# Record the start time
start_time = time.time()


#####################################################################################################################
####################################################----INPUTS----###################################################
#####################################################################################################################

dataset = 'DATASET_7'

#####################################################################################################################
####################################################----DEFINITIONS----###############################################
#####################################################################################################################


def make_mesh_dict_from_files(path):
    '''
    DESCRIPTION: makes a dictionary of meshes from json files of meshes
    INPUT: folder path
    OUTPUT: the dictionary of meshes with performance analysis
    '''
    # get filenames from main_path folder
    files = os.listdir(path)

    # make into mesh
    mesh_data = {}
    for file_name in files:
        mesh_name = file_name[:-10]
        mesh_data[mesh_name]={}
        filepath_mesh = os.path.join(path,file_name)

        with open(filepath_mesh, 'r') as file:
            mesh_data[mesh_name] = json.load(file)
    return mesh_data

def extract_keys_from_nested_dict(pa_dict, pa_keys):
    '''
    DESCRIPTION: Extract out the necessary performance criteria keys (Stability, Strength, Stiffness)
    INPUT: pa_dict is the performance analysis dictionary created from the definition make_mesh_dict_from_files()
    '''
    # Extract out the necessary performance criteria keys (Stability, Strength, Stiffness)
    pa_dict_sss = {mesh: {key: pa_dict[mesh][key] for key in pa_keys} for mesh in pa_dict}
    

    # Check whether there is failure in Stability or Strength (Stiffness check is already done)
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
main_path = os.path.join(os.getcwd(),'DATASETS/')
main_path_pa = os.path.join(main_path,dataset,'01_performance_evaluation/dataset_separate/')

# path for fixed supports
path_fixed_supports = os.path.join(main_path_pa,'fixed_support_no_walls/')
# path for pinned supports
path_pinned_supports = os.path.join(main_path_pa,'pinned_support_no_walls/')


# keys for SSS
keys_sss  = ['Buckling_Load_Factor','Utilization','Interstorey_Drift_Ratios', 'Interstorey_Drift_Failure']
# keys for pinned support vs fixed support comparison
keys_ss = ['Buckling_Load_Factor','Utilization', 'Max_Displacement/mm']

################## json to dictionary + extracting only SSS keys

# fixed supports
pa_supports_fixed = make_mesh_dict_from_files(path_fixed_supports)
pa_supports_fixed_sss = extract_keys_from_nested_dict(pa_supports_fixed, keys_sss)
pa_supports_fixed_ss = extract_keys_from_nested_dict(pa_supports_fixed, keys_ss)
#pinned supports
pa_supports_pinned = make_mesh_dict_from_files(path_pinned_supports)
pa_supports_pinned_sss = extract_keys_from_nested_dict(pa_supports_pinned, keys_sss)
pa_supports_pinned_ss = extract_keys_from_nested_dict(pa_supports_pinned, keys_ss)

# Convert nested dictionary to DataFrame
df_pa_supports_fixed_ss = pd.DataFrame.from_dict(pa_supports_fixed_ss)
df_pa_supports_pinned_ss = pd.DataFrame.from_dict(pa_supports_pinned_ss)

# Sort column names in ascending order considering numerical part
sorted_columns_fixed = sorted(df_pa_supports_fixed_ss.columns, key=lambda x: int(x.split('mesh_')[-1]))
sorted_columns_pinned = sorted(df_pa_supports_pinned_ss.columns, key=lambda x: int(x.split('mesh_')[-1]))
# Reorder DataFrame columns
df_pa_supports_fixed_ss = df_pa_supports_fixed_ss[sorted_columns_fixed]
df_pa_supports_pinned_ss = df_pa_supports_pinned_ss[sorted_columns_pinned]



#####################################################################################################################
####################################################----PLOT----#####################################################
#####################################################################################################################

plot_location = os.path.join(main_path,'plots', 'pinned_vs_fixed_supports', dataset)
# Create the '00_geometry_generation/footprint/' folder if it does not exist
if not os.path.exists(plot_location):
    os.makedirs(plot_location)


# Define custom color
colour_dark_blue = (11/255, 58/255, 64/255)  # Normalize RGB values to range [0, 1]
colour_teal = (15/255, 117/255, 118/255)  # Normalize RGB values to range [0, 1]
colour_maroon = (170/255, 80/255, 38/255)  # Normalize RGB values to range [0, 1]
colour_gold = (190/255, 181/255, 111/255)  # Normalize RGB values to range [0, 1]
colour_orange= (241/255, 118/255, 34/255)  # Normalize RGB values to range [0, 1]

colour_list = [colour_teal, colour_orange, colour_maroon]
# Define colors for each dataset
colors = [colour_orange, colour_gold ,colour_teal]

######################## pinned vs fixed support

# getting the buckling and utilization from the fixed dataset
buckling_fix = list(df_pa_supports_fixed_ss.loc['Buckling_Load_Factor'])
util_fix = list(df_pa_supports_fixed_ss.loc['Utilization'])
displacement_fix = list(df_pa_supports_fixed_ss.loc['Max_Displacement/mm'])

# getting the buckling and utilization from the pinned dataset
buckling_pin = list(df_pa_supports_pinned_ss.loc['Buckling_Load_Factor'])
util_pin = list(df_pa_supports_pinned_ss.loc['Utilization'])
displacement_pin = list(df_pa_supports_pinned_ss.loc['Max_Displacement/mm'])

# mesh names (columns)
mesh_names = list(df_pa_supports_fixed_ss.columns)
mesh_names = [i[5:] for i in mesh_names]

# buckling graph
plt.plot(mesh_names,buckling_fix, label = 'buckling_fixed_supports', color = colour_teal)
plt.plot(mesh_names,buckling_pin, label = 'buckling_pinned_supports', color = colour_orange)
plt.xlabel('mesh')
plt.ylabel('Buckling_Loading_Factor')
plt.title('Pinnned_vs_Fixed: Stability')
plt.legend()
plt.savefig(os.path.join(plot_location, f'plot_pa_supports_buckling.png'), dpi=300)
plt.show()

# utilization graph
plt.plot(mesh_names,util_fix, label = 'utilization_fixed_supports',color = colour_teal)
plt.plot(mesh_names,util_pin, label = 'utilization_pinned_supports',color = colour_orange)
plt.xlabel('mesh')
plt.ylabel('Utilization')
plt.title('Pinnned_vs_Fixed: Strength')
plt.legend()
plt.savefig(os.path.join(plot_location, f'plot_pa_supports_utilization.png'), dpi=300)
plt.show()

# displacement graph
plt.plot(mesh_names,displacement_fix, label = 'displacement_fixed_supports',color = colour_teal)
plt.plot(mesh_names,displacement_pin, label = 'displacement_pinned_supports',color = colour_orange)
plt.xlabel('mesh')
plt.ylabel('Max_Displacement / mm')
plt.title('Pinnned_vs_Fixed: Stiffness')
plt.legend()
plt.savefig(os.path.join(plot_location, f'plot_pa_supports_displacement.png'), dpi=300)
plt.show()

####################################################

# Average difference in pinned vs fixed



for key in keys_ss:

    avg_pin = (df_pa_supports_pinned_ss.loc[key].tolist())
    avg_pin =sum( avg_pin)/len(avg_pin)
    avg_fix = (df_pa_supports_fixed_ss.loc[key].tolist())
    avg_fix = sum(avg_fix)/len(avg_fix)

    diff = abs(avg_fix - avg_pin)
    avg = (avg_fix+ avg_pin)/2

    percentage_difference = (diff*100)/avg

    print(f"{key} Percentage difference = {percentage_difference} % ")





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