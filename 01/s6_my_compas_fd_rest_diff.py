import rhino3dm as rs
import compas
import compas_fd
from compas.datastructures import Mesh
import time
# from s1_crease_calculator import x,y,x_size,y_size,row_df,col_df
from compas.geometry import Point, Pointcloud, Line
# from compas_plotters import Plotter
import random
# from s5_fd_rest import master_mesh_dict_3
# from s0_edge_groups import dataset_id
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



'''INPUT VARIABLES ARE BELOW IN LOOP'''

# print(master_mesh_dict_1)

#####################################################################################################################
####################################################----SOLVER----################################################
#####################################################################################################################

from compas_fd.fd import fd_numpy 

def get_compas_meshes(x_size, y_size, x_div, y_div, master_mesh_dict_3, load_all, col_df, row_df):
    # FDM is implemented using NumPy, not available with RHino's IronPython, so a Proxy is needed
    # from compas.rpc import Proxy


        
    # opening the Proxy takes time (a couple of seconds), but, once open, form finding is fast
    # with Proxy('compas_fd.fd') as fd:

    master_mesh_dict_overall = {}
    master_mesh_dict_2 = {}
    for mesh_local in master_mesh_dict_3:
        
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
        forcedensities = [1] * len(edges)

        #'''ASSIGNING FORCE DENSITIES TO SPECIFIC EDGES'''

        i = 0
        fdict = {}

        #'''COLUMN EDGES'''
        for r_c_i, row_col in enumerate(master_mesh_dict_3[mesh_local]):
            if r_c_i == 0:
                for index, fd_col in enumerate(master_mesh_dict_3[mesh_local][r_c_i]):
                    index = f"col_{index+1}"
                    edges_col = col_df[index].tolist()

                    # assign force density of 2 to specific edges 
                    specific_edges = edges_col
                    for i, (u, v) in enumerate(edges):
                        if i in specific_edges:
                            forcedensities[i] = fd_col

            elif r_c_i == 1:
            #'''ROW EDGES'''    
                for index, fd_row in enumerate(master_mesh_dict_3[mesh_local][r_c_i]):
                    index = f"row_{index+1}"
                    edges_row = row_df[index].tolist()
                    
                    # assign force density of 2 to specific edges 
                    specific_edges = edges_row
                    for i, (u, v) in enumerate(edges):
                        if i in specific_edges:
                            forcedensities[i] = fd_row




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
    
    master_mesh_dict_overall['meshes'] = master_mesh_dict_2
    master_mesh_dict_overall['edges'] = edges 
    return master_mesh_dict_overall
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



# # main file path
# dataset_path_addition= os.path.join('DATASETS/',f"{dataset_id}/")
# main_path = os.path.join(os.getcwd(), dataset_path_addition)
# main_path = os.path.join(main_path,'00_geometry_generation/')
# mesh_path = os.path.join(main_path,'mesh/') 
# main_path = mesh_path
# # Create the '00_geometry_generation/mesh/' folder if it does not exist
# if not os.path.exists(mesh_path):
#     os.makedirs(mesh_path)







# for mesh_local,mesh in master_mesh_dict_2.items():
#     # specific_path_mesh
#     additional_string_mesh = f"{mesh_local}.json"
#     result_path_mesh = os.path.join(main_path,additional_string_mesh)
#     #result path
#     mesh.to_json(result_path_mesh)

#     # specific_path_edges
#     additional_string_edges = f"{mesh_local}_edges.json"
#     #result path
#     result_path_edges= os.path.join(main_path,additional_string_edges)
#     with open(result_path_edges, 'w') as json_file:
#         json.dump(edges,json_file, indent = 1)

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

