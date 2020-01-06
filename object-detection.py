# import the libraries
import torch
from torch.autograd import Variable
import cv2
from data import BaseTransform, VOC_CLASSES as labelmap
from ssd import build_ssd
import imageio

# Defining a function that will do the detections
def detect(frame, net, transform):
    # get the frame
    height, width = frame.shape[:2]

    # applied the transformation and convert to numpy array
    frame_t = transform(frame)[0]

    # second transformation convert numpy array in tensor
    x = torch.from_numpy(frame_t).permute(2, 0, 1)

    # third transformation: neural network only accept the batch
    # & last transformation: convert the batch in torch variable
    x = Variable(x.unsqueeze(0))
    y = net(x)
    
    # Next step Tensor and data
    detections = y.data
    scale = torch.Tensor([width, height, width, height])
    
    # detections = [batch, number of classes, number of ocurrence, [score, x0, y0, x1, y1]]
    for i in range(detections.size(1)):
        j = 0
        while detections[0, i, j, 0] >= 0.6:
            pt = (detections[0, i, j, 1:] * scale).numpy()

            # using openCV to draw the rectangle
            cv2.rectangle(frame, (int(pt[0]), int(pt[1])) , (int(pt[2]), int(pt[3])), (255, 0, 0), 2)
            cv2.putText(frame, labelmap[i-1], (int(pt[0]), int(pt[1])),
                cv2.FONT_HERSHEY_SIMPLEY, 2, (255, 255, 255), 2, cv2.LINE_AA)
            j += 1

    return frame

# Creating the SSD Neural Network
net = build_ssd('test')

net.load_state_dict(torch.load('ssd300_mAP_77.43_v2.pth', map_location = lambda storage, loc:storage))

# Creating the transformation
transform = BaseTransform(net.size, (104/256.0, 117/256.0, 123/256.0))

# Doing some object detection on a video
# imageio is the greate to manipulating video
reader = imageio.get_reader('funny_dog.mp4')
# fps = reader.get_meta_data()['fps']
# writer = imageio.get_writer('output.mp4', fps = fps)

# for i, frame in enumerate(reader):
#     frame = detect(frame, net.eval(), transform)
#     # Apend to write video
#     writer.append_data(frame)
#     print(i)

# Close the process
# writer.close()