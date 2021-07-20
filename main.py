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

    # if coord0 > 480 and coord1 < 640:
    #     coords = (480, coord1)
    # elif coord0 > 480 and coord1 > 640:
    #     coords = (480, 640)
    # elif coord0 < 480 and coord1 < 640:
    #     coords = (coord0, coord1)
    # elif coord0 < 480 and coord0 > 640:
    #     coords = (coord0, 640)
    # else:
    #     pass
    if coord0 > 640 and coord1 < 480:
        coords = (640+160, coord1)
    elif coord0 > 640 and coord1 > 480:
        coords = (640+160, 480)
    elif coord0 < 640 and coord1 < 480:
        coords = (coord0, coord1)
    elif coord0 < 640 and coord0 > 480:
        coords = (coord0, 480)
    else:
        pass

    # coords = (560, 360)
    # print(im.shape)
    g = int(math.ceil(coords[0] / (480 / 3)))
    f = int(math.ceil(coords[1] / (640 / 5)))
    # print(f, g)
    # print(a, b)
    # print(coords[0]/3, coords[1]/5)
    x1 = f * (480 / 3)
    y1 = (g - 1) * (640 / 5)
    x2 = x1 - (480 / 3)
    y2 = y1 + (640 / 5)

    x = (int(y1), int(x1))
    y = (int(y2), int(x2))
    return y, x

# 3D Model Points of selected landmarks in an arbitrary frame of reference
def get3dModelPoints():
  modelPoints = [[0.0, 0.0, 0.0],
                 [0.0, -330.0, -65.0],
                 [-225.0, 170.0, -135.0],
                 [225.0, 170.0, -135.0],
                 [-150.0, -150.0, -125.0],
                 [150.0, -150.0, -125.0]]
  return np.array(modelPoints, dtype=np.float64)


# 2D landmark points from all landmarks
def get2dImagePoints(shape):
  imagePoints = [[shape.part(30).x, shape.part(30).y],
                 [shape.part(8).x, shape.part(8).y],
                 [shape.part(36).x, shape.part(36).y],
                 [shape.part(45).x, shape.part(45).y],
                 [shape.part(48).x, shape.part(48).y],
                 [shape.part(54).x, shape.part(54).y]]
  return np.array(imagePoints, dtype=np.float64)


# Camera Matrix from focal length and focal center
def getCameraMatrix(focalLength, center):
  cameraMatrix = [[focalLength, 0, center[0] / 2],
                  [0, focalLength, center[1] / 2],
                  [0, 0, 1]]
  return np.array(cameraMatrix, dtype=np.float64)


# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
PREDICTOR_PATH = r"D:\reposetory\facemetric\common\shape_predictor_68_face_landmarks.dat"
SKIP_FRAMES = 20

try:
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Check if OpenCV is able to read feed from camera
    if (cap.isOpened() is False):
        print("Unable to connect to camera")
        sys.exit(0)

    # Just a place holder. Actual value calculated after 100 frames.
    fps = 30.0

    # Get first frame
    #ret, im = cap.read()

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_PATH)

    # initiate the tickCounter
    t = cv2.getTickCount()
    count = 0

    while True:
        # start tick counter if count is zero
        if count == 0:
            t = cv2.getTickCount()

        # Grab a frame
        ret, image = cap.read()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Process frames at an interval of SKIP_FRAMES.
        # This value should be set depending on your system hardware
        # and camera fps.
        # To reduce computations, this value should be increased
        if (count % SKIP_FRAMES == 0):
            # detect faces in the grayscale image
            faces = detector(gray, 0)

        # get 3D model points
        modelPoints = get3dModelPoints()

        # loop over the face detections
        for face in faces:
            x1 = int(face.left())
            y1 = int(face.top())
            x2 = int(face.right())
            y2 = int(face.bottom())

            # Сглаживание лица
            # im[y1:y2, x1:x2] = cv2.GaussianBlur(im[y1:y2, x1:x2], (15, 15), 0)
            # Не создает артефактов
            # im[y1:y2, x1:x2] = cv2.medianBlur(im[y1:y2, x1:x2], 5)
            gray[y1:y2, x1:x2] = cv2.bilateralFilter(gray[y1:y2, x1:x2], 9, 75, 75)

            # Face bbox
            # cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # determine the facial landmarks for the face region, then
            shape = predictor(gray, face)
            # draw a lines
            renderFace(image, shape)

            # get 2D landmarks from Dlib's shape object
            imagePoints = get2dImagePoints(shape)

            rows, columns = gray.shape
            focalLength = columns
            cameraMatrix = getCameraMatrix(focalLength, (rows, columns))

            # Assume no lens distortion
            distCoeffs = np.zeros((4, 1), dtype=np.float64)

            success, rotationVector, translationVector = cv2.solvePnP(modelPoints, imagePoints, cameraMatrix,
                                                                      distCoeffs)

            # Project a 3D point (0, 0, 1000.0) onto the image plane.
            # We use this to draw a line sticking out of the nose
            noseEndPoints3D = np.array([[0, 0, 1000.0]], dtype=np.float64)
            noseEndPoint2D, jacobian = cv2.projectPoints(noseEndPoints3D, rotationVector, translationVector,
                                                         cameraMatrix, distCoeffs)

            # points to draw line
            p1 = (int(imagePoints[0, 0]), int(imagePoints[0, 1]))
            p2 = (int(noseEndPoint2D[0, 0, 0]), int(noseEndPoint2D[0, 0, 1]))

            zone = get_zone(p2, gray)
            print(zone, " - coords rectangle!!!!!!!!!!!!!!")
            print(p2, " - coords p2")

            a, b = zone[0]
            c, d = zone[1]
            if a > 640 or b > 480 or c > 640 or d > 480 or a < 0 or b < 0 or c < 0 or d < 0:
                pass
            else:
                cv2.rectangle(image, zone[1], zone[0], (0, 255, 0), 3)
            #cv2.rectangle(image, zone[0], zone[1], (0, 255, 0), 3)
            # draw line using points P1 and P2
            cv2.line(image, p1, p2, (110, 220, 0), thickness=2, lineType=cv2.LINE_AA)

            # Print actual FPS
            # cv2.putText(image, "fps: {}".format(fps), (50, image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            imDisplay = cv2.resize(image, None, fx=0.5, fy=0.5)

            # show the output image with the face detections + facial landmarks
            cv2.imshow("webcam Head Pose", imDisplay)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            sys.exit()
    cv2.destroyAllWindows()
    cap.release()
except Exception as e:
    print(e)