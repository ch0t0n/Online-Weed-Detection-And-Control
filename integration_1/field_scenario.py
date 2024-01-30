from shapely.geometry import Polygon
import ast
import numpy as np
import os

v = [(0,0),(0,2),(2,2),(2,0)]

pol = Polygon(v)


# p1, p2 = (0,0), (2,2)
# x = euclidean_distance(p1, p2, 2)
# print(x)

def von_neumann_neighborhood(p, delta): # Von Neumann Neighborhood around a point of distance delta
    neighborhood = [p]
    x, y = p
    neighborhood.append((x+delta, y))
    neighborhood.append((x-delta, y))
    neighborhood.append((x, y+delta))
    neighborhood.append((x, y-delta))
    return neighborhood

def box_delta(p, delta):
    x, y = p
    box_points = [(x+delta, y+delta), (x-delta, y+delta), (x-delta, y-delta), (x+delta, y-delta)]
    return box_points

# p1 = (2, 3)
# delta = 5
# x = von_neumann_neighborhood(p1, 5)
# print(x)

class Field_Scenario: # Field scenario FS(Polygon,delta,image_data)
    # def __init__(self, polygon, delta, image_data) -> None:
    #     self.polygon = polygon
    #     self.delta = delta
    #     self.image_data = image_data
    
    def read(self, file): # Read the field data from a file
        with open(file) as f:
            data = f.read()
        values = ast.literal_eval(data) # Load the data from the file
        self.polygon = Polygon(values['polygon']) # Make the polygon from the vertices
        self.delta = values['delta'] 
        self.image_data = values['image_data']
        self.k1 = values['k1']
    
    def validate(self): # Check if the field scenario contains valid data. Run it after reading data from a file
        print('Checking if data is loaded or not')
        if self.image_data and self.delta and self.polygon:
            print('Data loaded successfully!')
            image_locations = [x[0] for x in self.image_data]
            for i, l in enumerate(image_locations):
                rect_points = box_delta(l, self.delta) # make a box of delta around each location
                rect = Polygon(rect_points)
                intersect = rect.intersection(self.polygon)
                if not intersect.area: # Check if the box intersects with the given polygon
                    # print('The image in location ', l, ' is not within the given polygon. Hence, removing it!')
                    self.image_data[i] = 0
                
                neighbor_points = von_neumann_neighborhood(l, self.delta)
                flag = False
                for v in neighbor_points:
                    if v in image_locations: # Check if any neighborhood point is within the image data
                        flag = True
                if not flag:
                    print('ERROR: the image location', l , ' does not have any other location within its delta-neighborhood!')
                    return 0
            self.image_data = [x for x in self.image_data if x]
        else:
            print('ERROR: data load unsuccessful! Either needs to read the data or the file contains incomplete data.')
            return 0
        print('All checks passed. The field scenario is loaded and valid!')
        return 1
    
    def image_location(self, image):
        location = [x[0] for x in self.image_data if x[1]==image]
        return location
    
if __name__ == '__main__':
    example_file = os.path.join('Examples', '1', 'field_scenario.txt')
    FS = Field_Scenario()
    FS.read(example_file)
    FS.validate()
    print(FS.image_data[0])



        

