import pandas as pd
import matplotlib.pyplot as plt
# import mplcursors
import plotly.graph_objects as go


plotting_dict = {'DATASET_9/': {'buckling': [2.52884, 4.791245, 4.984055, 5.429605, 5.940227, 6.548733, 7.278137, 7.701668, 8.163291, 8.680869, 9.134857, 2.702351, 9.744636, 10.457931, 11.232854, 12.129689, 13.125216, 14.126158, 15.208781, 16.453977, 17.851497, 19.48049, 2.892497, 3.103423, 3.312745, 3.517695, 3.746084, 3.991901, 4.279446, 4.611138], 'utilization': [3.454555, 2.102619, 2.044913, 1.86786, 1.68254, 1.507716, 1.468706, 1.416734, 1.371789, 1.329132, 1.288071, 3.215294, 1.241054, 1.19876, 1.228544, 1.186323, 1.134078, 1.083953, 1.001626, 0.940794, 0.892239, 0.841887, 2.948861, 2.754036, 3.127182, 2.946656, 2.729467, 2.548462, 2.367947, 2.192111], 'height': [0.402372, 0.5984, 0.614147, 0.648266, 0.6864, 0.7293, 0.777919, 0.804744, 0.833485, 0.864355, 0.897599, 0.416743, 0.933503, 0.972399, 1.014678, 1.060799, 1.111314, 1.166879, 1.228294, 1.296532, 1.372799, 1.458599, 0.432177, 0.4488, 0.466752, 0.4862, 0.507339, 0.5304, 0.555657, 0.58344], 'mesh': ['mesh_0', 'mesh_10', 'mesh_11', 'mesh_12', 'mesh_13', 'mesh_14', 'mesh_15', 'mesh_16', 'mesh_17', 'mesh_18', 'mesh_19', 'mesh_1', 'mesh_20', 'mesh_21', 'mesh_22', 'mesh_23', 'mesh_24', 'mesh_25', 'mesh_26', 'mesh_27', 'mesh_28', 'mesh_29', 'mesh_2', 'mesh_3', 'mesh_4', 'mesh_5', 'mesh_6', 'mesh_7', 'mesh_8', 'mesh_9']}, 'DATASET_10/': {'buckling': [11.998733, 32.978814, 33.103876, 33.148862, 33.898965, 33.541006, 32.532604, 31.293927, 29.294706, 26.812485, 18.463742, 11.742838, 13.237678, 13.222818, 13.125104, 13.068039, 13.059346, 12.614392, 11.8249, 10.96929, 10.641133, 11.86154, 11.382459, 10.955576, 10.524637, 9.987218, 9.415462, 9.042897, 9.98092, 18.627192], 'utilization': [8.114936, 3.284125, 2.966455, 2.826073, 2.830497, 2.611526, 2.321051, 2.114113, 1.939154, 1.84043, 2.171316, 8.401624, 10.445811, 
10.461208, 10.420829, 10.388816, 10.278128, 10.178003, 9.985343, 8.728558, 6.149951, 2.253877, 8.7441, 9.226592, 9.812653, 10.338855, 10.474554, 9.548059, 5.480582, 1.029491], 'height': [0.952329, 1.400602, 1.408144, 1.41734, 1.4288, 1.443478, 1.462952, 
1.49003, 1.541118, 1.634778, 1.816515, 0.976042, 0.706875, 0.719806, 0.735566, 0.755197, 0.78361, 0.821529, 0.87432, 0.952892, 
1.097505, 1.459731, 1.004356, 1.038755, 1.081434, 1.135782, 1.207329, 1.322259, 1.521514, 1.836756], 'mesh': ['mesh_0', 'mesh_10', 'mesh_11', 'mesh_12', 'mesh_13', 'mesh_14', 'mesh_15', 'mesh_16', 'mesh_17', 'mesh_18', 'mesh_19', 'mesh_1', 'mesh_20', 'mesh_21', 'mesh_22', 'mesh_23', 'mesh_24', 'mesh_25', 'mesh_26', 'mesh_27', 'mesh_28', 'mesh_29', 'mesh_2', 'mesh_3', 'mesh_4', 'mesh_5', 'mesh_6', 'mesh_7', 'mesh_8', 'mesh_9']}}


# # Define colors for each dataset
# colors = ['blue', 'red']

# # Plotting
# fig, ax = plt.subplots()

# # Plot points for each dataset
# scatter_handles = []
# for i, (dataset, data) in enumerate(plotting_dict.items()):
#     scatter = ax.scatter(data['height'], data['buckling'], color=colors[i], label=dataset)

#     # Annotate points with mesh names, height, and utilization
#     for j, (x, y, mesh) in enumerate(zip(data['height'], data['buckling'], data['mesh'])):
#         ax.annotate(f"{dataset}: {mesh}\nHeight: {x}m\nBuckling: {y}", (x, y),
#                     textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

#     scatter_handles.append(scatter)

# # Add labels
# plt.xlabel('Height of Vault')
# plt.ylabel('Buckling')

# # Add legend
# plt.legend()

# # Show the plot
# plt.show()





# Define colors for each dataset
colors = ['blue', 'red']

# Create a figure
fig = go.Figure()

# Plot points for each dataset
for i, (dataset, data) in enumerate(plotting_dict.items()):
    fig.add_trace(go.Scatter(x=data['height'], y=data['buckling'], mode='markers', name=dataset, marker=dict(color=colors[i])))

# Add hover text
hover_text = []
for dataset, data in plotting_dict.items():
    hover_text.extend([f"{dataset}: {mesh}<br>Height: {height}m<br>Buckling: {buckling}" for mesh, height, buckling in zip(data['mesh'], data['height'], data['buckling'])])

fig.update_traces(text=hover_text, hoverinfo='text')

# Set axis labels
fig.update_layout(xaxis_title='Height of Vault', yaxis_title='Buckling')

# Show the plot
fig.show()