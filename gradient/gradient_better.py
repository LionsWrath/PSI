import cv2
import argparse
import numpy as np
from random import randint
import matplotlib.pyplot as plt

def generateRGB():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)

    return [r, g, b]

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--width", type=int, 
        help="The Width of the image.",default=15)
parser.add_argument("-e", "--height", type=int, 
        help="The Height of the image.", default=18)
parser.add_argument("-p", "--pixel", type=int, 
        help="The Size of the pixel", default=25)

#> Colors
parser.add_argument("-c1", "--color1", help="Color on upper left", 
        default = generateRGB())
parser.add_argument("-c2", "--color2", help="Color on upper right",
        default = generateRGB())
parser.add_argument("-c3", "--color3", help="Color on lower left",
        default = generateRGB())
parser.add_argument("-c4", "--color4", help="Color on lower right",
        default = generateRGB())

args = parser.parse_args()

#---------------------------------------------------------------------

def createColorBlock(color):
    block = np.zeros((psize, psize,3), np.uint8)
    block[:,:,:3] = color

    return block

def createColorColumn(gradient):
    base = [createColorBlock(gradient[0])]
    [base.append(np.vstack((base[-1], createColorBlock(c)))) for c in gradient[1:]]

    return base[-1]

def createImage(colors):
    base = [createColorColumn(colors[0])]
    [base.append(np.hstack((base[-1], createColorColumn(g)))) for g in colors[1:]]

    return base[-1]

def cvtHEX2RGB(hex):
    if not isinstance(hex, (str,bytes)):
        return hex
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def create_gradient(origin, destiny, quantity):
    o = cvtHEX2RGB(origin)
    d = cvtHEX2RGB(destiny)

    gradient_r = np.linspace(o[0], d[0], quantity)
    gradient_g = np.linspace(o[1], d[1], quantity)
    gradient_b = np.linspace(o[2], d[2], quantity)

    return np.column_stack((
                gradient_r, 
                gradient_g, 
                gradient_b))

#---------------------------------------------------------------------

psize = args.pixel
sx,sy = (args.width, args.height)

ctop = create_gradient(args.color1, args.color2, sx)
cbot = create_gradient(args.color3, args.color4, sx)

colors = [create_gradient(t, b, sy) for t,b in zip(ctop, cbot)]
img = createImage(colors)

cv2.imwrite('gradient.jpg', img)
cv2.imshow('gradient', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
