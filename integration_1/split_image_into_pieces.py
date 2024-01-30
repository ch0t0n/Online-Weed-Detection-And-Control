from PIL import Image
from itertools import product
import matplotlib.pyplot as plt
import os
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10
plt.rcParams["figure.autolayout"] = True

os.chdir('..')
BASE_DIR = os.getcwd()
print(BASE_DIR)

# Inputs
field_picture = "DJI_0373-crop.JPG"
delta = 200
polygon = [(200,200), (200,600), (600,1000), (1600,800), (1800,200)]
example_path = os.path.join("Examples", "1")

# Output file
output_file = os.path.join(example_path, "field_scenario.txt")

try:
    os.remove(output_file)
except:
    pass

f = open(output_file, "a")

def split_image(image_name, d):
    name, ext = os.path.splitext(image_name)
    image = Image.open(os.path.join(BASE_DIR, example_path, image_name))
    w, h = image.size
    print("height of image = ", h, "width of image = ", w)
    x = len(range(0, w-w%d, d))
    y = len(range(0, h-h%d, d))
    print("Total x points = ", x)
    print("Total y points = ", y)
    print("total number of images = ", x * y)

    grid = product(range(0, w-w%d, d), range(0, h-h%d, d))
    sorted_grid = sorted((list(grid)))
    print(sorted_grid)
    try:
        os.mkdir(os.path.join(example_path, name+"_cropped"))
    except:
        pass

    fig = plt.figure(layout = "constrained")
    n = 1
    images_with_locations = []
    field_data = {"polygon": polygon, "delta": delta, "image_data": images_with_locations}
    for i in range(0, w-w%d, d):
        for j in range(0, h-h%d, d):
            box = (i, j, i+d, j+d)
            new_file_name = f"{name}_{i}_{j}{ext}"            
            out = os.path.join(example_path, name+"_cropped", new_file_name)
            images_with_locations.append([(i,j), out])
            cropped_image = image.crop(box)
            cropped_image.save(out)
            fig.add_subplot(x, y, n)
            plt.xticks([])
            plt.yticks([])
            plt.xlabel(str((i,j)))
            plt.imshow(cropped_image)
            n += 1
    f.write(str(field_data))
    f.close()
    plt.show()

split_image(field_picture, delta)