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

# Create the SSD Neural Network


