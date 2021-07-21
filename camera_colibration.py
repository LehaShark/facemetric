import numpy as np
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
