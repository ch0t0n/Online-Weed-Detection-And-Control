import os
import zmq
import secrets
import pickle

project_path = "/Users/choton/Library/CloudStorage/OneDrive-KansasStateUniversity/PhD_Research/Projects/Weed_Control_Project_2023/"
example_path = os.path.join(project_path, 'Examples', '15')

images_path = os.path.join(example_path, 'DJI_0373-crop_cropped')
images = os.listdir(images_path)


context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    to_send = secrets.choice(images)    
    print("Sending request %s …" % to_send)
    socket.send_string(to_send)

    # Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))