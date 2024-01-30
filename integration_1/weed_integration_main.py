import os
import sys
import numpy as np

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

# Euclidean distance between two points
def euclidean_distance(p1, p2, n): 
    dist_sum = 0
    for i in range(n):
        dist_sum += (p1[i]-p2[i])**2
    distance = np.sqrt(dist_sum)
    return distance

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
    os.chdir('./Examples')
    pwd = os.getcwd()
    example_file = os.path.join(pwd, '14', 'field_scenario4.txt')
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
    polygon, delta = list(FS.polygon.exterior.coords), FS.delta
    cell_lines, coverage_paths = optimal_coverage_paths(polygon, delta, k1)    

    print('\n ********* Coverage paths *********')
    for path in coverage_paths:
        print(path)

    # Compute the images of the paths
    paths_with_images = [[] for path in coverage_paths]
    for i, path in enumerate(coverage_paths):
        for j, v in enumerate(path):
            k = 0
            while True:
                img_v = FS.image_data[k][0]
                if euclidean_distance(img_v, v, 2) < delta:
                    paths_with_images[i].append([v,FS.image_data[k][1]])
                    break
                k += 1

    print('\n ********* Coverage paths with images *********')
    for path in paths_with_images:
        print(path)

    # new_coverage_paths = [[] for p in coverage_paths]
    # for i, path in enumerate(reversed(coverage_paths)):
    #     new_path = [v for v in path for j in range(i+1)]
    #     new_coverage_paths[i] = new_path

    visualize = Visualize(polygon, cell_lines, coverage_paths, paths_with_images)
    coverage_runtime = visualize.motion(0.01)

    print('\nCoverage Runtime = ', coverage_runtime, " seconds!")


    # Compute the spraying paths (weed_map, k2)
    weed_map = os.path.join(pwd, '14', '4.ini')
    
    blockPrint()
    os.chdir('../Codes')
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