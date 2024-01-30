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
sys.path.append('Codes/ag_coverage_new')
from coverage_main import *

# Import the spraying module
spraying_path = 'Codes/Ratan_code/mqrppwr/version2'
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
        # print(poly)
        coverage_obj = Coverage_Path_Planning(list(poly), delta, vs)
        curr_path = coverage_obj.sweep_coverage_path()
        k_paths.append(curr_path)
    return cell_lines, k_paths



# Drive function
if __name__ == "__main__":
    example_file = 'Examples/1/field_scenario3.txt'
    # Load the field scenario and read the example file
    FS = Field_Scenario()
    FS.read(example_file)
    isValid = FS.validate()
    if not isValid:
        print('The field scenario is not valid! Exiting the program')
        sys.exit(0)
    # print(FS.image_data)

    # Number of survey robots
    k1 = FS.k1

    print('Field images = ', FS.image_data)
    print('Polygon = ', FS.polygon)

    # Compute the optimal coverage paths (polygon, delta, k)
    polygon, delta = list(FS.polygon.exterior.coords), FS.delta/20
    cell_lines, coverage_paths = optimal_coverage_paths(polygon, delta, k1)
    print('\n ********* Coverage paths *********')
    for p in coverage_paths:
        print(p)
    visualize = Visualize(polygon, cell_lines, coverage_paths)
    coverage_runtime = visualize.motion(0.03)

    print('\nCoverage Runtime = ', coverage_runtime, " seconds!")


    # Compute the spraying paths (weed_map, k2)
    os.chdir('./Codes')
    pwd = os.getcwd()
    weed_map = os.path.join(pwd, 'Ratan_code', 'mqrppwr', 'version2', 'configuration', 'set-1', '2.ini')
    
    blockPrint()
    spraying_scenario, spraying_paths, actions, spraying_time = spraying_path(weed_map)  
    enablePrint()
    print('\nSpraying Scenario = ', spraying_scenario)

    # Number of spraying robots
    k2 = len(spraying_scenario[1])

    print('\n********* Spraing paths *********')
    for p in spraying_paths.values():
        print(p)   

    max_coverage_path = max([len(p) for p in coverage_paths])
    max_spraying_path = max([len(p) for p in spraying_paths.values()])

    print('\nTotal spraying time = ', spraying_time)

    output_str = '\nExperiment, No. of survey robots (K1), No. of sprayer robots (K2), Maximum coverage path length, Maximum spraying path length, Coverage runtime, Weed detection runtime, Spraying runtime\n'
    output_str += '1'+','+str(k1)+','+str(k2)+','+str(max_coverage_path)+','+str(max_spraying_path)+','+str(coverage_runtime)+','+'?'+','+str(spraying_time)+'\n'

    print(output_str)

    with open('outputs/Experiment_1.csv', "a") as w:
        w.write(output_str)