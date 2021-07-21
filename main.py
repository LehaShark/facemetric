import sys
import dlib
import cv2
import numpy as np
from renderFace import renderFace
from render_grid import render_rec, get_zone
from camera_colibration import getCameraMatrix, get2dImagePoints, get3dModelPoints

RESIZE_HEIGHT = 320

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
PREDICTOR_PATH = r"common/shape_predictor_68_face_landmarks.dat"
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
    ret, im = cap.read()

    if ret == True:
        height = im.shape[0]
        # calculate resize scale
        RESIZE_SCALE = float(height) / RESIZE_HEIGHT
        size = im.shape[0:2]
    else:
        print("Unable to read frame")
        sys.exit(0)

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

            # Draw all areas
            render_rec(image)

            zone = get_zone(p2, gray)

            # print(zone, " - coords rectangle!!!!!!!!!!!!!!")
            # print(p2, " - coords p2")

            zoneY1, zoneX1 = zone[0]
            zoneY2, zoneX2 = zone[1]

            # Draw area of interest
            if zoneY1 > image.shape[1] or zoneX1 > image.shape[0] or zoneY2 > image.shape[1] or zoneX2 > image.shape[0] or zoneY1 < 0 or zoneX1 < 0 or zoneY2 < 0 or zoneX2 < 0:
                pass
            else:
                cv2.rectangle(image, zone[1], zone[0], (0, 0, 255), 3)

            # draw line using points P1 and P2
            cv2.line(image, p1, p2, (110, 220, 0), thickness=2, lineType=cv2.LINE_AA)

            # Print actual FPS
            # cv2.putText(image, "fps: {}".format(fps), (50, image.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            imDisplay = cv2.resize(image, None, fx=0.5, fy=0.5)

            # show the output image with the face detections + facial landmarks
            cv2.imshow("webcam Head Pose", image)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            sys.exit()
    cv2.destroyAllWindows()
    cap.release()
except Exception as e:
    print(e)