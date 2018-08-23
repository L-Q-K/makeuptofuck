import cv2
import numpy
import glob

path = "picture/" + "eyebrow" + "/"
ind = glob.glob(path + "*")[2][-5]
print(ind)