import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-f","--filename", help="Name of the file", default="lena.jpg")
args = parser.parse_args()

def chroma420(img):
    imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    Y,CR,CB = cv2.split(imgYCC)

    Cr = np.repeat(CR[::2,::2], 2, axis=1)
    Cr = np.repeat(Cr, 2, axis=0)

    Cb = np.repeat(CB[::2,::2], 2, axis=1)
    Cb = np.repeat(Cb, 2, axis=0)

    Cr = resizeToIMG(img, Cr)
    Cb = resizeToIMG(img, Cb)

    stk = np.dstack((Y, Cr, Cb))
 
    return cv2.cvtColor(stk, cv2.COLOR_YCR_CB2BGR)

def chroma411(img):
    imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    Y,CR,CB = cv2.split(imgYCC)

    Cr = np.repeat(CR[::,::4], 4, axis=1)
    Cb = np.repeat(CB[::,::4], 4, axis=1)

    Cr = resizeToIMG(img, Cr)
    Cb = resizeToIMG(img, Cb)

    stk = np.dstack((Y, Cr, Cb))
    
    return cv2.cvtColor(stk, cv2.COLOR_YCR_CB2BGR)

def chroma422(img):
    imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    Y,CR,CB = cv2.split(imgYCC)

    Cr = np.repeat(CR[::,::2], 2, axis=1)
    Cb = np.repeat(CB[::,::2], 2, axis=1)

    Cr = resizeToIMG(img, Cr)
    Cb = resizeToIMG(img, Cb)

    stk = np.dstack((Y, Cr, Cb))
    
    return cv2.cvtColor(stk, cv2.COLOR_YCR_CB2BGR)

def chroma440(img):
    imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    Y,CR,CB = cv2.split(imgYCC)

    Cr = np.repeat(CR[::2,::], 2, axis=0)
    Cb = np.repeat(CB[::2,::], 2, axis=0)

    Cr = resizeToIMG(img, Cr)
    Cb = resizeToIMG(img, Cb)

    stk = np.dstack((Y, Cr, Cb))
    
    return cv2.cvtColor(stk, cv2.COLOR_YCR_CB2BGR)

def chroma410(img):
    imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    Y,CR,CB = cv2.split(imgYCC)

    Cr = np.repeat(CR[::2,::4], 4, axis=1)
    Cr = np.repeat(Cr, 2, axis=0)
    Cb = np.repeat(CB[::2,::4], 4, axis=1)
    Cb = np.repeat(Cb, 2, axis=0)

    Cr = resizeToIMG(img, Cr)
    Cb = resizeToIMG(img, Cb)

    stk = np.dstack((Y, Cr, Cb))
    
    return cv2.cvtColor(stk, cv2.COLOR_YCR_CB2BGR)

def resizeToIMG(ref, dst):
    height, width, _ = ref.shape
    return cv2.resize(dst, (width, height),
            interpolation=cv2.INTER_CUBIC)

img = cv2.imread(args.filename)

img420 = chroma420(img)
img411 = chroma411(img)
img422 = chroma422(img)
img440 = chroma440(img)
img410 = chroma410(img)

uimg = np.hstack((img,      img420))
uimg = np.hstack((uimg,     img411))
limg = np.hstack((img422,   img440))
limg = np.hstack((limg,     img410))
img =  np.vstack((uimg,     limg))

cv2.imshow('Multiple Results', img)

while True:
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()
