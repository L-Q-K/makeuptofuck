import cv2
import numpy

img = cv2.imread("download.png")
cv2.imshow("download", img)

print(img[:, :, 2])

cv2.waitKey()