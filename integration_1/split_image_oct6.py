from PIL import Image
from itertools import product
import matplotlib.pyplot as plt
import os
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10
plt.rcParams["figure.autolayout"] = True

BASE_DIR = os.getcwd()
print(BASE_DIR)

# Inputs
field_picture = "field.png"
delta = 20
k1 = 3
polygon = p2 = [[256.6593079432548, 399.99999999999994], [201.25432171493048, 387.80242003971586], [162.51309878474538, 372.78997053284024], [76.4332016181257, 336.31540469313137], [7.209123202696496, 255.0367331885686], [0.0, 237.53831348226328], [4.732747412572736, 204.6115650486281], [14.854041631532017, 138.2666330695749], [16.845264839560492, 125.5039073356404], [80.8251223252284, 58.665935751614995], [137.88382551360075, 0.0], [316.0731102295915, 56.51448549407656], [363.8382169296304, 107.55003010775243], [388.88935848808666, 143.30045234082297], [399.7030156903378, 164.1180841887105], [400.0, 234.1181171179687], [345.41782118038793, 331.23966951774673], [334.44550998663686, 343.87414375579726], [316.69676898920727, 361.5761248331441], [263.2590577628967, 395.9540467545297]]
example_path = os.path.join("Examples", "222")

# Output file
output_file = os.path.join(example_path, "field_scenario2.txt")

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
    field_data = {"k1": k1, "delta": delta, "polygon": polygon, "image_data": images_with_locations}
    for i in range(0, w-w%d, d):
        for j in range(0, h-h%d, d):
            box = (i, j, i+d, j+d)
            new_file_name = f"{name}_{i//10}_{j//10}{ext}"            
            out = os.path.join(example_path, name+"_cropped", new_file_name)
            images_with_locations.append([(i//10,j//10), out])
            cropped_image = image.crop(box)
            cropped_image.save(out)
            # fig.add_subplot(x, y, n)
            # plt.xticks([])
            # plt.yticks([])
            # plt.xlabel(str((i,j)))
            # plt.imshow(cropped_image)
            n += 1
    f.write(str(field_data))
    f.close()
    # plt.show()

split_image(field_picture, int(delta*9.9))