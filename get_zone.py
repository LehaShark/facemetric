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

        # coords = (560, 360)
        # print(im.shape)
        x_rec = (imX / 5)
        y_rec = (imY / 3)
        #g = int(math.ceil(coords[0] / (480 / 3)))
        #f = int(math.ceil(coords[1] / (640 / 5)))
        g = int(math.ceil(coordY / y_rec))
        f = int(math.ceil(coordX / x_rec))
        # print(f, g)
        # print(a, b)
        # print(coordY/3, coordX/5)
        x1 = f * y_rec
        y1 = (g - 1) * x_rec
        x2 = x1 - y_rec
        y2 = y1 + x_rec

        x = (int(y1), int(x1))
        y = (int(y2), int(x2))
        return y, x
