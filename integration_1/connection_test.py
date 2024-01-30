import os
import zmq
import secrets
import time

project_path = "/Users/choton/Library/CloudStorage/OneDrive-KansasStateUniversity/PhD_Research/Projects/Weed_Control_Project_2023/"
example_path = os.path.join(project_path, 'Examples', '11')
images_path = os.path.join(example_path, 'DJI_0373-crop_cropped')
images = os.listdir(images_path)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://*:5556")
time.sleep(1)

def simple_publisher(string):    
    # Serialize and send the list of strings
    socket.send_string(string)
    # socket.close()


for request in range(10):
    to_send = secrets.choice(images)    
    print("Sending request %s …" % to_send)
    simple_publisher(to_send)
    