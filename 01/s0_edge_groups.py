import numpy
import time
from pprint import pprint
import json
import csv
import os

import pandas as pd


print('-----------------------------------EDGE GROUPS.PY STARTS HERE--------------------------------------')

# Record the start time
start_time = time.time()


#####################################################################################################################
####################################################----DEFINITION----################################################
#####################################################################################################################

def edge_list_start_stop(x_val,y_val):

    '''
    DESCRIPTION:
    this gives the total number of edges and the range of edges in each column x.
    
    INPUT: 
    y_val is the number of squares in y direction. y is a positive integer.
    x_val is the number of squares in x direction. x is a positive integer.

    OUTPUT:
    dict_edge_list is a dictionary that contains the following keys:
    total_number_of_edges is the total number of edges,
    column_edge_start is the dictionary containing the range of each column x of the edge.
    

    #Example: x_val=15, y_val=4, 

    {'total_number_of_edges': 138, 'column_edge_start': {'col_1': (0, 8), 'col_2': (9, 17), 'col_3': (18, 26), 'col_4': (27, 35), 'col_5': (36, 44), 'col_6': (45, 53), 'col_7': (54, 62), 'col_8': (63, 71), 'col_9': (72, 80), 'col_10': (81, 89), 'col_11': (90, 98), 'col_12': (99, 107), 'col_13': (108, 116), 'col_14': (117, 125), 'col_15': (126, 134)}}

    this shows that column 0 has 0-8 edges, column 2 has 9-17 edges etc.
    '''

    start = 0
    end = start + 2*y_val 
    x_count = range(0,x_val)

    edge_list_of_start_end = []

    for i in x_count:
        n = i + 1
        edge_list_of_start_end.append((start,end))
        start = end + 1
        end = start + 2*y_val
    

    total_number_of_edges = edge_list_of_start_end[-1][1] + y_val



    # for dictionary output
    dict_edge_list = {}
    dict_edge_list['columns']={}
    dict_edge_list['rows']={}
    dict_edge_list['columns']['total_number_of_edges']= total_number_of_edges
    dict_edge_list['columns']['edge_start']= {}
    dict_edge_list['columns']['bool_list']= {}
    dict_edge_list['columns']['number_list'] = {}

    for i, val in enumerate(edge_list_of_start_end):

        dict_edge_list['columns']['edge_start'][f"col_{i+1}"] = val
        dict_edge_list['columns']['bool_list'][f"col_{i+1}"] = []
        dict_edge_list['columns']['number_list'][f"col_{i+1}"] = []

    

    return dict_edge_list


def even_odd_boolean(number):
    '''
    DESCRIPTION: outputs 1 if the input number is odd and 0 if it is even
    '''
    if number % 2 == 0:
        bool_no = 0
    else:
        bool_no = 1
    return bool_no


def pattern_merge(patt_1, patt_2, t_length):
    '''
    DESCRIPTION: 
    merges two patterns into one. Pattern 1 is an initial pattern that does not repeat. Pattern 2 is a pattern that repeats itself until the target length is satisfied.

    INPUT: 
    
    patt_1 = [A,B,C]. it is a pattern
    patt_2 = [1,2,3]. it is a pattern
    t_length = 10. it is a target length
    
    OUTPUT:
    [A,B,C,1,2,3,1,2,3,1]
    '''

    # pattern_1 occurs once + whole pattern_2 repeats until whole number + part of pattern_2 remainder
    merged_pattern = patt_1 + (patt_2 * (t_length // len(patt_2))) + patt_2[:t_length % len(patt_2)] 
    # refining to fit the target length
    merged_pattern = merged_pattern[:t_length]

    return merged_pattern


def get_edge_numbers_from_pattern(input_pattern_dictionary, input_start_edge_dictionary, t_length, column_row):
    '''
    DESCRIPTION: 
    
    INPUTS:
    input_pattern_dictionary is a dictionary whose keys are rows/ column numbers and values are the final pattern adjusted to the target length
    input_start_edge_dictionary is dictionary whose keys are rows/ column numbers and values are the starting edge numbers of each column/row

    example: 
    data['columns']['bool_list'] is the input dictionary

    '''
    output_directory = {}
    last_col_list = []
    for col_num, pattern in input_pattern_dictionary.items():
        edge_list_numbers = []
        n=1

        start_loc = input_start_edge_dictionary[col_num][0]
        # stop_local = data['columns']['edge_start'][col_num][1]

        for i in pattern:
            start_loc = start_loc + i
            edge_list_numbers.append(start_loc)
            n+=1
            
            # if start_loc >= stop_local:
            if n >= t_length:
                break
        output_directory[col_num] = edge_list_numbers


    if column_row in ['column', 'Column','COLUMN']:
        col_num_last = (f"{col_num[:4]}{(len(output_directory.keys()) + 1)}")

        for i in range(1,t_length,1):

            start_edge_of_last = int(output_directory[f"{col_num[:4]}{(len(output_directory.keys()))}"][-1] ) + 2
            
            start_edge_of_last = start_edge_of_last + i 
            last_col_list.append(start_edge_of_last)

        output_directory[col_num_last] = last_col_list


    return output_directory




#####################################################################################################################
####################################################----INPUTS----###################################################
#####################################################################################################################

# y = 15
# x= 10

def get_polyedges(x,y):

    #####################################################################################################################
    ####################################################----OVERALL-SOLVER----############################################
    #####################################################################################################################

    data = (edge_list_start_stop(x,y))

    row_increment = data['columns']['edge_start']['col_1'][1] + 2

    #####################################################################################################################
    ####################################################----PATTERNS----#################################################
    #####################################################################################################################

    '''
    PATTERN A - column patterns
    # pattern A of col_2 repeats for all col numbers onwards
    '''

    pattern_A = {}
    pattern_A['col_1']= {}
    pattern_A['col_2']= {}

    # first pattern happens once. second pattern repeats onwards 
    pattern_A['col_1']['first'] = [1,2,2,2,2,2,2]
    pattern_A['col_1']['second'] = [2,2,2,2,2,2,2]

    pattern_A['col_2']['first'] = [0,2,2,2,2,2,2]
    pattern_A['col_2']['second'] = [2,2,2,2,2,2,2]

    '''
    PATTERN A - row patterns
    # pattern A of row_1 repeats for all row numbers onwards until last row
    differences between rcol_1 and col_1 is
    a) first edge order is flipped so starting edge is bottom one instead of left side
    b) order of 3 and 1 is shifted in all
    c) ending pattern of last even/odd edges is added. In this case of pattern A it is always [2]. No ending pattern exists in col_1,col_2 etc 
    '''

    pattern_A['row_1']= {}
    pattern_A['row_2']= {}
    # rcol represents the pattern of the starting edge numbers for each row
    pattern_A['rcol_1'] = {}
    # pattern is similar to the pattern from the col_1. see above description
    pattern_A['rcol_1']['first'] = [0,2,2,2,2,2,2]
    pattern_A['rcol_1']['second'] = [2,2,2,2,2,2,2]
    # pattern of row_1 repeats itself until the 6th edge (one below the 3). pattern of row_2 happens in 6th and 7th edge
    pattern_A['row_1']['first'] = [0,row_increment]
    pattern_A['row_1']['second'] = [row_increment - 1]
    pattern_A['row_2']['first'] = [0,row_increment - 1]
    pattern_A['row_2']['second'] = [row_increment - 1]





    #####################################################################################################################
    ####################################################----COLUMN-SOLVER----############################################
    #####################################################################################################################




    polyedge_dict = {}

    # number of edges in y direction
    target_length = y+1 

    ########## getting the final pattern for each column inside the data 

    for col_num in data['columns']['edge_start']:
        
        # start and end edge of the pattern
        start_local = data['columns']['edge_start'][col_num][0]
        stop_local = data['columns']['edge_start'][col_num][1]


        # # checking the column number so odd columns eg col_1 can represent an even boolean (0) in the pattern
        # col = int(col_num[4:]) + 1

        # from col_2 onwards, pattern remains the same 
        if col_num == 'col_1':
            col_num_pattern = 'col_1'
        else: 
            col_num_pattern = 'col_2'


        # patterns
        pattern_1 = pattern_A[col_num_pattern]['first']
        pattern_2 = pattern_A[col_num_pattern]['second']

    
        # boolean list from pattern
        bool_list = pattern_merge(pattern_1, pattern_2, target_length)

        # # adding the last edge pattern to the last edge
        # if col % 2 == 0:
        #     bool_list.append(2) if start_local % 2 == 0 else bool_list.append(1)
        # else:
        #     bool_list.append(2) if start_local % 2 == 1 else bool_list.append(1)

        data['columns']['bool_list'][col_num]= bool_list
            


    ########## mapping the final boolean pattern to get the edge numbers
    data['columns']['number_list'] = get_edge_numbers_from_pattern(data['columns']['bool_list'], data['columns']['edge_start'], target_length, 'column')       



    #####################################################################################################################
    ####################################################----ROW-SOLVER----############################################
    #####################################################################################################################


    ###########################################         for starting edges      ##########################################

    ########## getting the final boolean pattern for the starting edges of each row inside the data

    target_length = y

    # patterns
    pattern_1 = pattern_A['rcol_1']['first']
    pattern_2 = pattern_A['rcol_1']['second']

    # boolean list from pattern + ending pattern
    bool_list = pattern_merge(pattern_1, pattern_2, target_length) + [2]

    ########## mapping the final boolean pattern to get the edge numbers for the starting edges of each row inside the data

    rcol_edge_list_numbers = []

    start_local = data['columns']['edge_start']['col_1'][0]
    stop_local = data['columns']['edge_start']['col_1'][1]

    for i in bool_list:
        start_local = start_local + i
        rcol_edge_list_numbers.append(start_local)
        
        if start_local >= stop_local:
            break
    rcol_edge_list_numbers


    ###########################################         for row  edges      ##########################################



    # number of edges in x direction
    target_length = x

    ###################


    # Check if the difference between consecutive elements is 3
    differences_3 = [rcol_edge_list_numbers[i + 1] - rcol_edge_list_numbers[i] == 3 for i in range(len(rcol_edge_list_numbers) - 1)]
    differences_3.insert(0,False)

    # Make a boolean list for items having difference of 3  as well as those one edge preceeding 
    boolean_list = []
    for i in range(len(differences_3)):
        if differences_3[i] or (i < len(differences_3) - 1 and differences_3[i + 1]):
            boolean_list.append(1)
        else:
            boolean_list.append(0)

    # last two rows are also boolean 1
    boolean_list[-1]=1
    boolean_list[-2]=1



    ########## getting the final pattern for each row inside the data 

    data['rows']['edge_start'] = {}
    data['rows']['bool_list'] = {}
    data['rows']['number_list']= {}

    for i, start_local in enumerate(rcol_edge_list_numbers):
        
        data['rows']['edge_start'] [f"row_{i+1}"] = [start_local, 0]

        # if boolean is 0, row_1 pattern is used, but if boolean is 1 then row_2 is used. note that row_2 pattern doesn't mean the pattern is in row_2. it is just the second pattern.
        if boolean_list[i] == 1 and i==len(rcol_edge_list_numbers)-1:
            row_num_pattern = 'row_2'
        else: 
            row_num_pattern = 'row_1'


        # patterns
        pattern_1 = pattern_A[row_num_pattern]['first']
        pattern_2 = pattern_A[row_num_pattern]['second']

    
        # boolean list from pattern
        bool_list = pattern_merge(pattern_1, pattern_2, target_length)

        # # adding the last edge pattern to the last edge
        # if col % 2 == 0:
        #     bool_list.append(2) if start_local % 2 == 0 else bool_list.append(1)
        # else:
        #     bool_list.append(2) if start_local % 2 == 1 else bool_list.append(1)

        data['rows']['bool_list'][f"row_{i+1}"]= bool_list
            


    ########## mapping the final boolean pattern to get the edge numbers
    data['rows']['number_list'] = get_edge_numbers_from_pattern(data['rows']['bool_list'], data['rows']['edge_start'], target_length+1, 'row')       



    #####################################################################################################################
    ####################################################----CONVERT----#####################################################
    #####################################################################################################################


    row_dataframe = pd.DataFrame(data['rows']['number_list'])
    col_dataframe = pd.DataFrame(data['columns']['number_list'])


    polyedge_dict[f"col_df"]=col_dataframe
    polyedge_dict[f"row_df"]=row_dataframe
    return polyedge_dict


#####################################################################################################################
####################################################----TEST----#####################################################
#####################################################################################################################

# print(rcol_edge_list_numbers)
# print('------------------')
# print('------column boolean_list--------')
# print(data['columns']['bool_list'])
# print('----------------------')
# '------column number_list--------'
# print(data['columns']['number_list'])        
# print('----------------------')
# '------column_edge_start--------'
# print(data['columns']['edge_start'])      
# print('----------------------')
# '------rcol edge list numbers--------'
# print(rcol_edge_list_numbers)    
# print('----------------------')  
# '------row number_list--------'
# print(data['rows']['number_list'])
# print('----------------------')
# '------row_edge_start--------'
# print(data['rows']['edge_start'])      
# print('----------------------')    
# print('----------------------')
# '------row_boolean_list--------'
# print(data['rows']['bool_list'])      
# print('----------------------') 
# print('------col_dataframe--------')
# print(col_df)      
# print('----------------------')  
# print('------row_dataframe--------')
# print(row_df)      
# print('----------------------')    



#####################################################################################################################
####################################################----EXPORT----#####################################################
#####################################################################################################################

# # main file path
# dataset_id = 'DATASET_2'

# dataset_path_addition= os.path.join('DATASETS/',f"{dataset_id}/")
# main_path = os.path.join(os.getcwd(), dataset_path_addition)

# main_path = os.path.join(main_path,'00_geometry_generation/footprint/')

# # Create the '00_geometry_generation/footprint/' folder if it does not exist
# if not os.path.exists(main_path):
#     os.makedirs(main_path)




# # specific_path_rows
# additional_string_row = f"x={x},y={y}_row_dict.csv"
# #result path
# result_path_row = os.path.join(main_path,additional_string_row)
# print(result_path_row)

# # specific_path_rows
# additional_string_col = f"x={x},y={y}_col_dict.csv"
# #result path
# result_path_col = os.path.join(main_path,additional_string_col)

# # Export the DataFrame to a CSV file
# row_df.to_csv(result_path_row, index=False)
# col_df.to_csv(result_path_col, index=False)

#####################################################################################################################
####################################################----END----#####################################################
#####################################################################################################################

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

print('-----------------------------------EDGE GROUPS.PY ENDS HERE--------------------------------------')