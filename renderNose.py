import numpy as np
import cv2

def pose_estimate(image, landmarks):
    """
    Given an image and a set of facial landmarks generates the direction of pose
    """
    size = image.shape
    image_points = np.array([
        (landmarks[33, 0], landmarks[33, 1]),     # Nose tip
        (landmarks[8, 0], landmarks[8, 1]),       # Chin
        (landmarks[36, 0], landmarks[36, 1]),     # Left eye left corner
        (landmarks[45, 0], landmarks[45, 1]),     # Right eye right corner
        (landmarks[48, 0], landmarks[48, 1]),     # Left Mouth corner
        (landmarks[54, 0], landmarks[54, 1])      # Right mouth corner
        ], dtype="double")

    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (0.0, -330.0, -65.0),        # Chin
        (-225.0, 170.0, -135.0),     # Left eye left corner
        (225.0, 170.0, -135.0),      # Right eye right corner
        (-150.0, -150.0, -125.0),    # Left Mouth corner
        (150.0, -150.0, -125.0)      # Right mouth corner
        ])

    focal_length = size[1]
    center = (size[1]/2, size[0]/2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
        ], dtype="double")

    dist_coeffs = np.zeros((4, 1))
    success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    p1 = (int(image_points[0][0]), int(image_points[0][1]))
    p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
    return p1, p2