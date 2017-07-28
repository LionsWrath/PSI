import matplotlib.pyplot as plt
import numpy as np
import cv2

img = cv2.imread('lena.jpg')
imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

print imgYCC

cv2.imshow('Origi', img)
cv2.imshow('YCrCb', imgYCC)
cv2.waitKey(0)
cv2.destroyAllWindows()

