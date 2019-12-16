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
    
    # Next step
    detections = y.data
    scale = torch.Tensor([width, height, width, height])
    
