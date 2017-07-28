import numpy as np
import cv2

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


img = cv2.imread('chroma_2.jpg')

img420 = chroma420(img)
img411 = chroma411(img)
img422 = chroma422(img)
img440 = chroma440(img)
img410 = chroma410(img)

cv2.imshow('Output 420', img420)
cv2.imshow('Output 411', img411)
cv2.imshow('Output 422', img422)
cv2.imshow('Output 440', img440)
cv2.imshow('Output 410', img410)
cv2.imshow('Original', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
