import random 
import json
import os
from s0_edge_groups import dataset_id

# main file path
# main_path = 'D:/OneDrive - Delft University of Technology/Thesis/python/00_geometry_generation/dataset/'

dataset_path_addition= os.path.join('DATASETS/',f"{dataset_id}/")
main_path = os.path.join(os.getcwd(), dataset_path_addition)
main_path = os.path.join(main_path,'00_geometry_generation/dataset/')

# Create the '00_geometry_generation/footprint/' folder if it does not exist
if not os.path.exists(main_path):
    os.makedirs(main_path)



thickness_dataset = []
thickness = [35,60,95]
for i in range(0,10000):

    # Option 1: random from either [35,60,95]
    thickness_dataset.append(random.choice(thickness))

    # Option 2: random from any integer in range 35-95
    # thickness_dataset.append(random.randint(35,95))


    
# specific_path_thickness
additional_string = 'thickness_dataset.json'
#result path
result_path= os.path.join(main_path,additional_string)
with open(result_path, 'w') as json_file:
    json.dump(thickness_dataset,json_file, indent = 1)