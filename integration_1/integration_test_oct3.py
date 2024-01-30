import os
import sys

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__

# Import the field scenario class
from field_scenario import Field_Scenario

# Import the coverage module
sys.path.append('ag_coverage_new')
from coverage_main import *

# Import the spraying module
spraying_path = 'Ratan_code/mqrppwr/version2'
sys.path.append(spraying_path)
from spraying_module import *


# function to compute the coverage paths
def optimal_coverage_paths(polygon, delta, k):
    polygon = list(rounding_polygon(polygon))
    vs = 8
    cpp_object = Coverage_Path_Planning(polygon, delta, vs)
    cell_lines = cpp_object.decomposed_lines()
    area_set = cpp_object.calc_Cellareas()
    segmented_areas = Segmentation(area_set, k).opt_segments
    k_poly = k_polygons(segmented_areas, cell_lines)
    k_paths = []
    for poly in k_poly:
        print(poly)
        coverage_obj = Coverage_Path_Planning(list(poly), delta, vs)
        curr_path = coverage_obj.sweep_coverage_path()
        k_paths.append(curr_path)
    return k_paths

# function to compute the spraying paths
def optimal_spraying_paths(field_scenario, weed_map, k2):
    pass


# Drive function
if __name__ == "__main__":
    # Set the working directory
    os.chdir('..')
    example_file = os.path.join('Examples', '1', 'field_scenario.txt')

    # Load the field scenario and read the example file
    FS = Field_Scenario()
    FS.read(example_file)
    FS.validate()
    # print(FS.image_data)

    # Number of survey robots
    k1 = 3

    # Number of spraying robots
    k2 = 5

    # Compute the optimal coverage paths (polygon, delta, k)
    polygon, delta = list(FS.polygon.exterior.coords), FS.delta/20    
    coverage_paths = optimal_coverage_paths(polygon, delta, k1)
    print('\n********* Coverage paths *********')
    for p in coverage_paths:
        print(p)

    # Compute the spraying paths (weed_map, k2)
    os.chdir('./Codes')
    pwd = os.getcwd()
    weed_map = os.path.join(pwd, 'Ratan_code', 'mqrppwr', 'version2', 'configuration', 'set-1', '2.ini')
    print(weed_map)
    blockPrint()
    paths, actions = spraying_path(weed_map, k2)
    enablePrint()
    print('\n********* Spraing paths *********')
    for p in paths.values():
        print(p)


    # print(config_path))