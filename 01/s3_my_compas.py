import rhino3dm as rs
import compas
import compas_fd
from compas.datastructures import Mesh
import time
from s1_crease_calculator import x,y,x_size,y_size,row_df,col_df
from compas.geometry import Point, Pointcloud, Line
# from compas_plotters import Plotter
import random
from s2_crease_twin import master_mesh_dict_1, mesh_path
import json
import os




print('-----------------------------------MY_COMPAS.PY STARTS HERE--------------------------------------')

start_time = time.time()


#####################################################################################################################
####################################################----INPUT----################################################
#####################################################################################################################

# size of footprint in metres. already defined earlier 
# x_size = x
# y_size = y

# number of divisions in x and y. already defined earlier 
# x = 15
# y = 27

'''INPUT CONSTANTS'''
x_div =  x
y_div = y
load_all = 30.0

'''INPUT VARIABLES ARE BELOW IN LOOP'''

# print(master_mesh_dict_1)

#####################################################################################################################
####################################################----SOLVER----################################################
#####################################################################################################################

from compas_fd.fd import fd_numpy 

# FDM is implemented using NumPy, not available with RHino's IronPython, so a Proxy is needed
# from compas.rpc import Proxy


    
# opening the Proxy takes time (a couple of seconds), but, once open, form finding is fast
# with Proxy('compas_fd.fd') as fd:


master_mesh_dict_2 = {}
for mesh_local in master_mesh_dict_1:
    
    '''INPUT VARIABLES'''

    # generate a standard mesh grid
    mesh = Mesh.from_meshgrid(x_size, int(x_div), y_size, int(y_div))

    # get initial vertex coordinates
    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()]

    # get indices of fixed vertices (supports)
    fixed = mesh.vertices_on_boundary()

    # get edge connectivity
    edges = list(mesh.edges())

    # set load
    load = load_all

    # set forcedensities
    forcedensities = [master_mesh_dict_1[mesh_local]['fd_rest']] * len(edges)

    #'''ASSIGNING FORCE DENSITIES TO SPECIFIC EDGES'''

    i = 0
    fdict = {}
    

    #'''COLUMN EDGES'''
    for fd_col, edges_col in master_mesh_dict_1[mesh_local]['col'].items():
        # fdict[f"edge_{i}"] = edges
        # fdict[f"fd_{i}"] = int(fd[3:])
        # i+=1

        # assign force density of 2 to specific edges 
        specific_edges = edges_col
        for i, (u, v) in enumerate(edges):
            if i in specific_edges:
                forcedensities[i] = float(fd_col[3:])

    #'''ROW EDGES'''    
    for fd_row, edges_row in master_mesh_dict_1[mesh_local]['row'].items():
        # fdict[f"edge_{i}"] = edges
        # fdict[f"fd_{i}"] = int(fd[3:])
        # i+=1    
            
        # assign force density of 2 to specific edges 
        specific_edges = edges_row
        for i, (u, v) in enumerate(edges):
            if i in specific_edges:
                forcedensities[i] = float(fd_row[3:])




    # apply loads per vertex based on initial tributary area
    total_load = load
    mesh_area = mesh.area()
    loads = [(0.0, 0.0, total_load * mesh.vertex_area(vkey) / mesh_area) for vkey in mesh.vertices()]

    # form find!
    result = fd_numpy(vertices=vertices, fixed=fixed, edges=edges, forcedensities=forcedensities, loads=loads)

    # result data
    node_coordinates, node_residual_forces, edge_forces, edge_lengths = result

    # # convert to Rhino data
    # lines = [rs.AddLine(node_coordinates[u], node_coordinates[v]) for u, v in edges]

    lines = [Line(node_coordinates[u], node_coordinates[v]) for u, v in edges]
    # lines = lines[0],lines[2],lines[60],lines[58],lines[1],lines[57], lines[14], lines[115]

    for vkey, (x, y, z) in enumerate(node_coordinates):
        mesh.vertex[vkey]['x'] = x
        mesh.vertex[vkey]['y'] = y
        mesh.vertex[vkey]['z'] = z

    master_mesh_dict_2[mesh_local]= mesh
# print(mesh)


#####################################################################################################################
####################################################----PLOT----#####################################################
#####################################################################################################################

# plotter = Plotter()

# point_A = Point(0, 0, 0)
# point_B = Point(1, 1, 1)
# point_list = [point_A,point_B]
# point_cloud = Pointcloud.from_bounds(10, 10, 0, 100)


# line_1 = Line(point_A,point_B)


#plot point_cloud
# plotter.add_from_list(point_cloud, size=1, facecolor=(1.0, 0.7, 0.7), edgecolor=(1.0, 0, 0))

#plot multiple points
# plotter.add_from_list(point_list, size=1, facecolor=(1.0, 0.7, 0.7), edgecolor=(1.0, 0, 0))

# # plot single point
# plotter.add(point_A, size=10, facecolor=(1.0, 0.7, 0.7), edgecolor=(1.0, 0, 0))

# plot single line
# plotter.add_from_list(lines, 
#             linewidth=1.0,
#             linestyle='solid',
#             color=	(0.0, 0.0, 0.0),
#             draw_points=True)
# plotter.zoom_extents()
# plotter.show()


#####################################################################################################################
####################################################----EXPORT----#####################################################
#####################################################################################################################



# main file path
# main_path = 'D:/OneDrive - Delft University of Technology/Thesis/python/00_geometry_generation/mesh/'
main_path = mesh_path

for mesh_local,mesh in master_mesh_dict_2.items():
    # specific_path_mesh
    additional_string_mesh = f"{mesh_local}.json"
    result_path_mesh = os.path.join(main_path,additional_string_mesh)
    #result path
    mesh.to_json(result_path_mesh)

    # specific_path_edges
    additional_string_edges = f"{mesh_local}_edges.json"
    #result path
    result_path_edges= os.path.join(main_path,additional_string_edges)
    with open(result_path_edges, 'w') as json_file:
        json.dump(edges,json_file, indent = 1)

#####################################################################################################################
####################################################----TEST----#####################################################
#####################################################################################################################


# print('-------------')
# print(node_coordinates)
# print('-------------')
# print(mesh_local)
# print(item)
# print('------node_coordinates--------')
# print(node_coordinates[0])
# print('----------------------')
# print('------node_residual_forces--------')
# print(node_residual_forces[item])
# print('------edge_forces--------')
# print(edge_forces[item])
# print('----------------------')
# print('------edge_lengths--------')
# print(edge_lengths[item])
# print('----------------------')
# print('------force_densities--------')
# print(len(forcedensities))
# print('----------------------')
# print('------edges--------')
# print(edges)
# print('----------------------')
# print('------lines--------')
# print(lines)
# print('----------------------')


#####################################################################################################################
####################################################----END----#####################################################
#####################################################################################################################

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

print('-----------------------------------MY_COMPAS.PY ENDS HERE--------------------------------------')

