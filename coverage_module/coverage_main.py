import numpy as np
import polygenerator
from coverage_path_planning import *
from segmentation_using_dp import *

use_coppeliaSim_simulator = False  # To use CoppeliaSim simulator

if use_coppeliaSim_simulator:
    from drone_simulation import *
else:
    from visualization import *

def rounding_polygon(polygon):
    x, y = zip(*polygon)
    x = np.array(x)
    y = np.array(y)
    cx = np.mean(x)
    cy = np.mean(y)
    a = np.arctan2(y - cy, x - cx)
    order = a.ravel().argsort()
    x = x[order]
    y = y[order]
    vertices = list(zip(x, y))
    return vertices

def k_polygons(k_segments, cell_lines):
    cell_lines = [[list(x) for x in ele] for ele in cell_lines]
    # print('cell lines =', cell_lines)

    trapezoids = []
    for i in range(len(cell_lines) - 1):
        trapezoids.append([cell_lines[i][0], cell_lines[i][1], cell_lines[i+1][0], cell_lines[i+1][1]])
    # print('trapezoids = ', trapezoids)

    polygons = [[trapezoids.pop(0) for _ in seg] for seg in k_segments]

    polygons = [[line for sub in ele for line in sub] for ele in polygons]

    updated_polygon = [[] for _ in polygons]

    for i in range(len(polygons)):
        for j in range(len(polygons[i])):
            if j%2 == 0:
                updated_polygon[i].append(list(polygons[i][j]))
        for j in range(len(polygons[i]),-1,-1):
            if j%2 == 1:
                updated_polygon[i].append(list(polygons[i][j]))

    res = [[] for _ in updated_polygon]
    for i in range(len(updated_polygon)):
        for j in range(len(updated_polygon[i])):
            if updated_polygon[i][j] not in res[i]:
                res[i].append(updated_polygon[i][j])

    res = [rounding_polygon(x) for x in res]
    return res


# Driver code
def main():
    # polygon = polygenerator.random_convex_polygon(num_points = 20)    
    # print(x)
    # return 0
    # time.sleep(5)
    # polygon = [(10, 1), (14, 5), (13, 6), (7, 6), (1, 4), (4, 1)]
    # polygon = [(7,1), (7, 6), (1, 4), (4, 1)]
    # polygon = [(8, 1), (14,1), (15, 4), (13, 8), (7, 9), (1, 6), (1, 3)]
    # polygon = [(12, 1), (14, 4), (13, 9), (7, 8), (1, 5), (4, 1)]
    # polygon = [ (10, 2), (14, 4), (13, 8), (5, 9), (1, 5)]
    # polygon = [(1, 1), (10, 1), (10,10), (1,10)]
    # polygon = [(1, 1), (10, 1), (5,10)]
    # polygon = [(1, 1), (10, 1), (15,5), (5,5)]

    # Experiments
    # polygon = [(10, 1), (14, 5), (13, 8), (7, 10), (5, 10), (1, 2)]
    # polygon = [(10, 1), (14, 4), (13, 6), (7, 9), (1, 5), (4, 1)]
    # polygon = [(12, 1), (14, 4), (13, 9), (7, 8), (1, 5), (4, 1)]


    polygon = np.array([(0.5964754632713541, 1.0), (0.46025667769705403, 0.9996818709489957), (0.26481311444351396, 0.9950971284832629), (0.10334759743145677, 0.9440422908568102), (0.0, 0.9009650273669986), (0.042411169061821345, 0.764936050223613), (0.17165373130429895, 0.41492667596027893), (0.30997532033959396, 0.2135648027515077), (0.47618778406060225, 0.05802435794376881), (0.6181311842072998, 0.001613045609672859), (0.6341346471866985, 0.0), (0.8947336611491123, 0.2408828862226269), (0.9345350874125086, 0.28660771212603403), (0.9941653848749401, 0.43962710202625843), (0.9999999999999999, 0.4879646261511102), (0.9906919338737652, 0.6432022713946349), (0.9702830153393452, 0.7981373538390176), (0.8832733983468586, 0.9647509273229642), (0.783228269975197, 0.9825068533085446), (0.658542979784317, 0.9967863217489609)])
    polygon = polygon * 100
    polygon = list(polygon)

    print('Polygon = ', polygon)

    delta = 0.002 # Coverage parameter
    k = 10   # Number of robots
    vs = 8 # Average Velocity
    height = 0.35

    cpp_object = Coverage_Path_Planning(polygon, delta, vs)
    cell_lines = cpp_object.decomposed_lines()
    print('\nDecomposed lines = ', cell_lines)
    area_set = cpp_object.calc_Cellareas()
    segmented_areas = Segmentation(area_set, k).opt_segments
    print('\nsegmented area set = ', segmented_areas)

    polygons = k_polygons(segmented_areas, cell_lines)
    print('\npolygons =', polygons)

    k_paths = []
    for poly in polygons:
        # print(poly)
        coverage_obj = Coverage_Path_Planning(list(poly), delta, vs)
        curr_path = coverage_obj.sweep_coverage_path()
        k_paths.append(curr_path)

    inputs = []
    for i in k_paths:
        ui = cpp_object.calc_u(i)
        inputs.append(ui)
    # for i in inputs:
        # print('inputs for path ', inputs.index(i), 'is = ', i)

    if use_coppeliaSim_simulator: # CoppeliaSim Simulator
        drone_simulator = Drone_simulator(polygon, k_paths)
        drone_simulator.draw_field(height)
        drone_simulator.start_simulation()
        drone_simulator.simulate_path(height)
        time.sleep(500)
        drone_simulator.stop_simulation()
    else: # Visualizing the simulation using Matplotlib
        ts = delta / vs  # Time step
        visualize = Visualize(polygon, cell_lines, k_paths)
        with open('poly.txt', "a") as f:
            print('New polygon = ', polygon, file=f)
        # visualize.lines()  # For visualizing the lines
        visualize.motion(ts)  # For visualizing the motion


if __name__ == "__main__":
    main()