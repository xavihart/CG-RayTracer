import cv2
import numpy as np
path = "./checker-2048.ppm"
a = cv2.imread(path)
cv2.imwrite("./0004.jpg", a)