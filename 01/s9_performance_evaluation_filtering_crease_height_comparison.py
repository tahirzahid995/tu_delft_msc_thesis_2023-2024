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

datasets = ['DATASET_28']

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
    pa_dict[dataset] = extract_keys_from_nested_dict(pa_dict[dataset], keys_sss, 'pa')
    pa_dict[dataset] = pd.DataFrame.from_dict(pa_dict[dataset])

for dataset, path in main_path_dict['gg'].items():
    gg_height_dict[dataset] = make_mesh_dict_from_files(path, 'gg')
    gg_height_dict[dataset] = extract_keys_from_nested_dict(gg_height_dict[dataset], key_height, 'gg')
    gg_height_dict[dataset] = pd.DataFrame.from_dict(gg_height_dict[dataset])



#####################################################################################################################
####################################################----PLOT----#####################################################
#####################################################################################################################

plot_location = os.path.join(main_path,'plots/')
# Create the '00_geometry_generation/footprint/' folder if it does not exist
if not os.path.exists(plot_location):
    os.makedirs(plot_location)

################## extracting uniform force densties for each mesh

dataset_file_path = os.path.join(main_path, datasets[0], '00_geometry_generation\dataset\dataset.csv')
df = pd.read_csv(dataset_file_path)

fd_dict = {}
for mesh in df.columns:
    fd_dict[mesh] = df[mesh].iloc[0]



plotting_dict = {}
for dataset, dataframe in pa_dict.items(): 
    plotting_dict[dataset]= {}
    
    # getting the buckling, displacement, and utilization
    buckling = list(pa_dict[dataset].loc['Buckling_Load_Factor'])
    util= list(pa_dict[dataset].loc['Utilization'])
    displacement = list(pa_dict[dataset].loc['Interstorey_Drift_Ratios'])
    displacement = [float(i[0][:-1]) for i in displacement]

    # getting the height
    height_of_vault = list(gg_height_dict[dataset].loc['Height_of_vault/m'])

    # getting mesh names (columns)
    mesh_names = list(gg_height_dict[dataset].columns)

    plotting_dict[dataset]['buckling'] = buckling                #y axis
    plotting_dict[dataset]['utilization'] = util                 #y axis
    plotting_dict[dataset]['displacement'] = displacement        #y axis  
    plotting_dict[dataset]['height'] = height_of_vault           #x axis
    plotting_dict[dataset]['mesh']= mesh_names

fd_list=[]
for mesh in mesh_names:
    fd_list.append(fd_dict[mesh]) 
print(fd_list)
# ############################################################################## AVERAGE DATASET


# # plotting_dict['DATASET_25_high']['displacement'] = [0.000181]*20
# # plotting_dict['DATASET_25_medium']['displacement'] = [0.000125]*20
# # plotting_dict['DATASET_25_low']['displacement'] = [0.0000685]*20

# avg = {}
# for d in datasets:
#     avg[d]={}
#     avg[d]['buckling'] = sum(plotting_dict[d]['buckling'])
#     avg[d]['utilization'] = sum(plotting_dict[d]['utilization'])
#     avg[d]['displacement'] = sum(plotting_dict[d]['displacement'])



# # high seismic vs medium seismic
# avg_buckling_diff = (avg[datasets[0]]['buckling'] - avg[datasets[1]]['buckling'])/ len(plotting_dict[dataset]['buckling'])
# avg_util_diff = (avg[datasets[0]]['utilization'] - avg[datasets[1]]['utilization'])/ len(plotting_dict[dataset]['utilization'])
# avg_disp_diff = (avg[datasets[0]]['displacement'] - avg[datasets[1]]['displacement'])/ len(plotting_dict[dataset]['displacement'])

# # increase/reduce by % medium to high
# inc_buckling_ptg =round(avg_buckling_diff * 100/ (avg[datasets[1]]['buckling']/len(plotting_dict[dataset]['buckling'])),2)
# inc_util_ptg =round(avg_util_diff * 100/ (avg[datasets[1]]['utilization']/len(plotting_dict[dataset]['utilization'])),2)
# inc_disp_ptg =round(avg_disp_diff * 100/(avg[datasets[1]]['displacement']/len(plotting_dict[dataset]['displacement'])),2)

# print(f"---------------------------------------------------",'\n','-------------------------------')
# print(f"Medium to high seismic percentage reduction/increase")
# print(f"---------------------------------------------------")
# print(f"buckling: {inc_buckling_ptg} %")
# print(f"utilization: {inc_util_ptg} %")
# print(f"interstorey_drift: {inc_disp_ptg} %")

# # medium seismic vs low seismic
# avg_buckling_diff = (avg[datasets[1]]['buckling'] - avg[datasets[2]]['buckling'])/ len(plotting_dict[dataset]['buckling'])
# avg_util_diff = (avg[datasets[1]]['utilization'] - avg[datasets[2]]['utilization'])/ len(plotting_dict[dataset]['utilization'])
# avg_disp_diff = (avg[datasets[1]]['displacement'] - avg[datasets[2]]['displacement'])/ len(plotting_dict[dataset]['displacement'])


# # increase/reduce by % low to medium
# inc_buckling_ptg =round(avg_buckling_diff * 100/ (avg[datasets[2]]['buckling']/len(plotting_dict[dataset]['buckling'])),2)
# inc_util_ptg =round(avg_util_diff * 100/ (avg[datasets[2]]['utilization']/len(plotting_dict[dataset]['utilization'])),2)
# inc_disp_ptg =round(avg_disp_diff * 100/(avg[datasets[2]]['displacement']/len(plotting_dict[dataset]['displacement'])),2)

# print(f"---------------------------------------------------",'\n','-------------------------------')
# print(f"Low to Medium seismic percentage reduction/increase")
# print(f"---------------------------------------------------")
# print(f"buckling: {inc_buckling_ptg} %")
# print(f"utilization: {inc_util_ptg} %")
# print(f"interstorey_drift: {inc_disp_ptg} %")



############################################################################## HOVER GRAPH USING MPLCURSORS
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

# Plotting
fig, ax = plt.subplots()

# Plot points for each dataset
scatter_handles = []
for i, (dataset, data) in enumerate(plotting_dict.items()):
    scatter = ax.scatter(data['height'], data['utilization'], color=colors[i], label=dataset)
    scatter_handles.append(scatter)

# Annotate points with mesh names, height, and utilization
annot = mplcursors.cursor(scatter_handles, hover=True)
annot.connect("add", lambda sel: sel.annotation.set_text(
    f"{plotting_dict[sel.artist.get_label()]['mesh'][sel.target.index]}\n"
    f"Height: {plotting_dict[sel.artist.get_label()]['height'][sel.target.index]}m\n"
    f"Utilization: {plotting_dict[sel.artist.get_label()]['utilization'][sel.target.index]}"
))

# Add labels
plt.xlabel('Height of Vault/m')
plt.ylabel('Utilization')

# Add legend
plt.legend()

# Show the plot
plt.show()


##################################################### HEGIHT VS BUCKLING

# Plotting
fig, ax = plt.subplots()

# Plot points for each dataset
scatter_handles = []
for i, (dataset, data) in enumerate(plotting_dict.items()):
    scatter = ax.scatter(data['height'], data['buckling'], color=colors[i], label=dataset)
    scatter_handles.append(scatter)

# Annotate points with mesh names, height, and utilization
annot = mplcursors.cursor(scatter_handles, hover=True)
annot.connect("add", lambda sel: sel.annotation.set_text(
    f"{plotting_dict[sel.artist.get_label()]['mesh'][sel.target.index]}\n"
    f"Height: {plotting_dict[sel.artist.get_label()]['height'][sel.target.index]}m\n"
    f"Buckling: {plotting_dict[sel.artist.get_label()]['buckling'][sel.target.index]}"
))

# Add labels
plt.xlabel('Height of Vault/m')
plt.ylabel('Buckling')

# Add legend
plt.legend()

# Show the plot
plt.show()



##################################################### HEGIHT VS DISPLACEMENT

# Plotting
fig, ax = plt.subplots()

# Plot points for each dataset
scatter_handles = []
for i, (dataset, data) in enumerate(plotting_dict.items()):
    scatter = ax.scatter(data['height'], data['displacement'], color=colors[i], label=dataset)
    scatter_handles.append(scatter)

# Annotate points with mesh names, height, and utilization
annot = mplcursors.cursor(scatter_handles, hover=True)
annot.connect("add", lambda sel: sel.annotation.set_text(
    f"{plotting_dict[sel.artist.get_label()]['mesh'][sel.target.index]}\n"
    f"Height: {plotting_dict[sel.artist.get_label()]['height'][sel.target.index]}m\n"
    f"Interstorey_Drift_Ratios: {plotting_dict[sel.artist.get_label()]['displacement'][sel.target.index]}"
))

# Add labels
plt.xlabel('Height of Vault/m')
plt.ylabel('Interstorey_Drift_Ratios')

# Add legend
plt.legend()


# Define a custom formatter function
def format_y_ticks(y, pos):
    return f'{y}h'

# Apply the custom formatter to the y-axis ticks
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_y_ticks))

plt.show()


# Show the plot
plt.show()

############################################################################## HOVER GRAPH USING PLOTLY

# # Define colors for each dataset
# colors = ['blue', 'red']

# # Create a figure
# fig = go.Figure()

# # Plot points for each dataset
# for i, (dataset, data) in enumerate(plotting_dict.items()):
#     fig.add_trace(go.Scatter(x=data['height'], y=data['buckling'], mode='markers', name=dataset, marker=dict(color=colors[i])))

# # Add hover text
# hover_text = []
# for dataset, data in plotting_dict.items():
#     hover_text.extend([f"{dataset}: {mesh}<br>Height: {height}m<br>Buckling: {buckling}" for mesh, height, buckling in zip(data['mesh'], data['height'], data['buckling'])])

# fig.update_traces(text=hover_text, hoverinfo='text')

# # Set axis labels
# fig.update_layout(xaxis_title='Height of Vault', yaxis_title='Buckling')


# # fig.write_image(os.path.join(plot_location, f'height_vs_buckling_{datasets}.png'))

# # Show the plot
# fig.show()



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