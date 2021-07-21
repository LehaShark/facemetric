import cv2

# import the necessary packages
import math

def get_zone(coords, im):
    if im.shape[0] == 480 and im.shape[1] == 640:
        coordY = coords[0]
        coordX = coords[1]

        imY = im.shape[0]
        imX = im.shape[1]

        print(im.shape)
        if coordY > imX and coordX < imY:
            coords = (imX + (imX - imY), coordX)
        elif coordY > imX and coordX > imY:
            coords = (imX + (imX - imY), imY)
        elif coordY < imX and coordX < imY:
            coords = (coordY, coordX)
        elif coordY < imX and coordY > imY:
            coords = (coordY, imY)
        else:
            pass

        x_rec = (imX / 5)
        y_rec = (imY / 3)

        column = int(math.ceil(coordY / y_rec))
        row = int(math.ceil(coordX / x_rec))
        # print(row, column)

        x1 = row * y_rec
        y1 = (column - 1) * x_rec
        x2 = x1 - y_rec
        y2 = y1 + x_rec

        x = (int(y1), int(x1))
        y = (int(y2), int(x2))
        return y, x


def render_rec(image):
    x1, y1 = 0, int((image.shape[0]) / 3)
    x2, y2 = int((image.shape[1]) / 5), 0
    for i in range(17):
        if x2 <= image.shape[1]:
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
            print(image.shape)
            x1 += int((image.shape[1]) / 5)
            x2 += int((image.shape[1]) / 5)
        else:
            x1 = 0
            y1 += int((image.shape[0]) / 3)
            x2 = int((image.shape[1]) / 5)

# def render_rec(image):
#     x1, y1 = 0, (image.shape[0] / 3)
#     x2, y2 = (image.shape[1] / 5), 0
#     for i in range(17):
#         if x2 <= image.shape[1]:
#             cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
#             x1 += (image.shape[1] / 5)
#             x2 += (image.shape[1] / 5)
#         else:
#             x1 = 0
#             y1 += (image.shape[0] / 3)
#             x2 = (image.shape[1] / 5)