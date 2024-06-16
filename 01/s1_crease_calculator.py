import itertools
import math
import copy
from s0_edge_groups import data, x,y, row_df, col_df
import time


print('-----------------------------------CREASE CALCULATOR.PY STARTS HERE--------------------------------------')

start_time = time.time()

#####################################################################################################################
####################################################----DEFINITION----################################################
#####################################################################################################################

def remove_creases_below_threshold(combination, edges_to_skip_x):
    '''
    DESCRIPTION:
    Removes all consecutive edges below threshold limit

    example: 
    INPUTS: combination= [1,2,3,4,5] , edges_to_skip_x = 1
    OUTPUTS: [1,3,5]
    '''
    for i in range(len(combination)-1):
        j = i+1
        if combination[i]==combination[-1]:
            break
        if combination[j]-combination[i] <= edges_to_skip_x:
            del combination[j]
        if combination[i]==combination[-1]:
            break
    return combination


def continue_func_until_length_const(function_x, initial_data, function_dependency = None):
    '''
    DESCRIPTION: 
    Repeats a function on intial data until the length of output remains the same. This is useful for functions where the
    length of output and output needs to converge. A built_in redundancy has been added in case the function causes the 
    input length to change as well so a deepcopy of the input_length is made.

    example:

    INPUT:
    function = remove_creases_below_threshold
    initial data = [1,2.5,2.6,2.7,2.8,2.9,3,4,5,6,8.5,9,10.2,10.5,10.6,10.7]
    function_dependency = 1

    OUTPUT:
    [1, 2.5, 4, 6, 8.5, 10.2]
    '''
    previous_output = function_x(initial_data, function_dependency)
    while True:
        before_length = copy.deepcopy(len(previous_output))
        current_output =  function_x(previous_output,1)
        after_length = len(current_output)
        if after_length == before_length:
            break
    return current_output


def removing_inital_creases_below_threshold(x, edge_len_x, min_spacing_x):
    '''
    DESCRIPTION:
    Removes initial creases whose distance from the start/end of the vault is less than the minimum
    spacing.

    example:

    INPUT:
    x = [1,2,3,4,5,6,7,8,9,10] is a list of rows/columns 
    edge_len_x = 0.5 is the edge length 
    min_spacing_x = 2 is the minimum spacing between the start/end and the first edge

    OUTPUT:
    '''    
    removing_list = []
    new_x = []
    
    # makes a list of items that are to be removed
    for i,val in enumerate(x):
        j = i+1
        if min_spacing_x > edge_len_x*(i+1):
            removing_list.append(x[i])
            removing_list.append(x[-1*j])
        else:
            break
    
    # makes a list of items from the original list that are not found in the removing list
    for i,val in enumerate(x):
        if val not in removing_list:
            new_x.append(val)        
    return new_x


def making_combinations(x, min_threshold):
    '''
    DESCRIPTION: 
    An list of rows or columns is input. All possible combinations are generated. It is checked 
    whether the minimum distance between consecutive edges is satisfied by the minimum threshold. 
    If it is not satisfied then the edges are removed. Then, repetitions are removed from the list.

    example:

    INPUT: [1,2,3,4]

    OUPTUT: [[1], [2], [3], [4], [1, 4], [1, 3], [2, 4]]
    '''


    # making iterations
    # example if x = [1,2,3] then output = [(1,),(2,),(3,),(1,2),(2,3),(1,3)]
    combination_list = []
    for i in range(1,len(x)+1):
        for combination in itertools.combinations(x, i):
            combination_list.append(combination)
            
    # converting list of tuples of varying sizes into nested list i.e output = [[1],[2],[3],[1,2],[2,3],[1,3]]
    combination_list = [[i] if isinstance(i, int) else list(i)for i in combination_list ]

    # removing creases below the threshold spacing 
    clean_combination_list = []
    for combination in combination_list:
        clean_combination =  continue_func_until_length_const(remove_creases_below_threshold, combination, min_threshold)
        clean_combination_list.append(clean_combination)

    # removing repetitions
    deep_clean_combination_list = []
    for combination in clean_combination_list:
        if combination not in deep_clean_combination_list:
            deep_clean_combination_list.append(combination)

    # print(f"{len(combination_list) - len(deep_clean_combination_list)} combinations removed")
    return deep_clean_combination_list


#####################################################################################################################
####################################################----INPUTS----################################################
#####################################################################################################################


# size of footprint in metres
x_size = x
y_size = y

# number of divisions in x and y. already defined earlier 
# x = 15
# y = 27

# spacing between creases in metres
min_spacing = 3

#####################################################################################################################
####################################################----SOLVER----################################################
#####################################################################################################################


edge_length_row = x_size/x
edge_length_col = y_size/y

edges_to_skip_row = math.ceil(((min_spacing / edge_length_row) - 1))
edges_to_skip_col = math.ceil(((min_spacing / edge_length_col) - 1))

col_list = list(data['columns']['number_list'].keys())
row_list = list(data['rows']['number_list'].keys())

col_list = [int(i[4:]) for i in col_list]
row_list = [int(i[4:]) for i in row_list]


col_list_new = removing_inital_creases_below_threshold(col_list, edge_length_col, min_spacing)
row_list_new = removing_inital_creases_below_threshold(row_list, edge_length_row, min_spacing)

combination_col_list = making_combinations(col_list_new, min_spacing)
combination_row_list = making_combinations(row_list_new, min_spacing)


# col_? or row_?
# i = 2
# edges_from_col = data['columns']['number_list'][f"col_{i}"]




################# Removing symmetrical creases

# symmetrical column list
even =len(col_list)
odd = len(col_list)-1

if len(col_list)%2 == 0:
    col_list_symm = col_list[:even/2]
else:
    col_list_symm = col_list[:int(odd/2)]


# symmetrical row list
row_list
even =len(row_list)
odd = len(row_list)-1

if len(row_list)%2 == 0:
    row_list_symm = row_list[:int(even/2)]
else:
    row_list_symm = row_list[:int(odd/2)]



# Removal from column_combinations

combination_col_list_symm = []  
combination_col_list_symm_not = []  
for combination in combination_col_list:
    if any(i in combination for i in col_list_symm):
        combination_col_list_symm_not.append(combination)
    else:
        combination_col_list_symm.append(combination)


# Removal from column_combinations

combination_row_list_symm = []  
combination_row_list_symm_not = []  
for combination in combination_row_list:
    if any(i in combination for i in row_list_symm):
        combination_row_list_symm_not.append(combination)
    else:
        combination_row_list_symm.append(combination)



################## Making the mesh dictionary from column combinations
mesh_dict_col = {}
mesh_no = 0
# each combination happens in one mesh
for combination in combination_col_list:
    
    mesh_dict_col[f"mesh_col_{mesh_no}"] ={}

    # i represents the column_number (col_i) or row_number (row_i)
    for i in combination:
        
        # edges from each row/column of the combination
        edges_from_i = list(col_df[f"col_{i}"])

        mesh_dict_col[f"mesh_col_{mesh_no}"][f"col_{i}"] = edges_from_i

    mesh_no += 1




#####################################################################################################################
####################################################----TEST----#####################################################
#####################################################################################################################
# print('------mesh_dict_col--------')
# print(mesh_dict_col)
# print('------edges from combination_columns--------')
# print(edges_from_col)
# print('------number of column crease combinations--------')
# print(len(combination_col_list))
# print('------number of row crease combinations--------')
# print(len(combination_row_list))
# print('----------------------')
# print('------column crease combination list--------')
# print(combination_col_list[80])
# print('----------------------')
# print('------row crease combination list--------')
# print(combination_row_list)
# print('----------------------')
# print(col_list)
# print(col_list_symm)
# print(row_list)
# print(row_list_symm)
# print('----------------------')
# print('------combination column list symmetrical--------')
# print(len(combination_col_list_symm))
# print('----------------------')
# print('------combination column list non-symmetrical--------')
# print(len(combination_col_list_symm_not))
# print('----------------------')
# print('------combination row list symmetrical--------')
# print(len(combination_row_list_symm))
# print('----------------------')
# print('------combination row list non-symmetrical--------')
# print(len(combination_row_list_symm_not))
#####################################################################################################################
####################################################----END----#####################################################
#####################################################################################################################

# Record the end time
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time} seconds")

print('-----------------------------------CREASE CALCULATOR.PY ENDS HERE--------------------------------------')
