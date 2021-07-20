# import the necessary packages
import sys
#from imutils import face_utils
import dlib
import cv2
import numpy as np
import math
from renderFace import renderFace

def get_zone(coords, im):
    coord0 = coords[0]
    coord1 = coords[1]
    print(im.shape)
    if coord0 > im.shape[1] and coord1 < im.shape[0]:
        coords = (im.shape[1] + (im.shape[1] - im.shape[0]), coord1)
    elif coord0 > im.shape[1] and coord1 > im.shape[0]:
        coords = (im.shape[1] + (im.shape[1] - im.shape[0]), im.shape[0])
    elif coord0 < im.shape[1] and coord1 < im.shape[0]:
        coords = (coord0, coord1)
    elif coord0 < im.shape[1] and coord0 > im.shape[0]:
        coords = (coord0, im.shape[0])
    else:
        pass

    # coords = (560, 360)
    # print(im.shape)
    x_rec = (im.shape[1] / 5)
    y_rec = (im.shape[0] / 3)
    g = int(math.ceil(coords[0] / x_rec))
    f = int(math.ceil(coords[1] / y_rec))
    # print(f, g)
    # print(a, b)
    # print(coords[0]/3, coords[1]/5)
    x1 = f * x_rec
    y1 = (g - 1) * y_rec
    x2 = x1 - x_rec
    y2 = y1 + y_rec

    x = (int(y1), int(x1))
    y = (int(y2), int(x2))
    return y, x
