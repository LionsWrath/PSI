import cv2
import numpy as np
import matplotlib.pyplot as plt

from numpy import random as rnd

def hex_to_RGB(hex):
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
        "{0:x}".format(v) for v in RGB])

#---------------------------------------------------------------------

def color_dict(gradient):
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
	"r":[RGB[0] for RGB in gradient],
	"g":[RGB[1] for RGB in gradient],
     	"b":[RGB[2] for RGB in gradient]}


def linear_gradient(start_hex, finish_hex, n):
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)

    RGB_list = [s]

    for t in range(1, n):
        curr_vector = [int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) 
                for j in range(3)]

        RGB_list.append(curr_vector)

    return color_dict(RGB_list)

#---------------------------------------------------------------------

colors_top = linear_gradient('00DDCD', '982D75', 5)
colors_bot = linear_gradient('0023D2', 'BF007F', 5)

colors = np.column_stack((
    colors_top["hex"], 
    colors_bot["hex"], 
    range(len(colors_top["hex"]))))

NX = 250
NY = 250
img = np.zeros((NX, NY, 3), np.uint8)

for t,b,i in colors:
    lgrad = linear_gradient(t, b, 5)
    cgrad = np.column_stack((
        lgrad["r"], 
        lgrad["g"], 
        lgrad["b"], 
        range(len(lgrad["r"]))))

    for r,g,b,n in cgrad:
        y1 = 0  + (50 * i.astype(int)) %NX
        y2 = 50 + (50 * i.astype(int)) %NX

        x1 = 0  + (50 * n) %NY
        x2 = 50 + (50 * n) %NY

        img[x1:x2, y1:y2, 0:3] = np.array([b,g,r])

plt.imshow(img)
plt.show()
