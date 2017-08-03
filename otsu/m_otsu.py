import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="Name of the file", default="lena.jpg")
args = parser.parse_args()

#---------------------------------------------------------------------------------------------------

def apply(img, val):
    
    def process(x, v, lut):
        if x < v:
            return lut[x]
        else:
            return x

    hist,_ = np.histogram(img.flatten(), 256, [0,256])
    cdf = hist.cumsum()

    # Calculate lut of the dark region
    # Normalize the lut
    lut = np.ma.masked_equal(cdf, 0)
    lut = (lut - lut.min()) * 255 / (lut.max() - lut.min())
    lut_m = np.ma.filled(lut, 0).astype('uint8')

    vfunc = np.vectorize(process, excluded=[2,3], otypes=[np.uint8]) 

    return vfunc(img, val, lut_m)

def calculateVariance(p, w, q):
    avg = np.sum(p*w)/q
    var = np.sum(((w-avg)**2)*(p/q))

    return var

def otsu(img):
    norm,bins = np.histogram(img.flatten(), 
            bins=np.arange(256), 
            density=True)                                   # Calculate normalized histogram
    bins = bins[:-1]                                        # Bin size correction
    cdf = norm.cumsum()                                     # Cumulative distributive function

    res = [(np.inf, -1)]
    for i in bins:
        pl,pr = np.hsplit(norm, [i])                        # Divide the probabilities
        wl,wr = np.hsplit(bins, [i])                        # Get the weights
        ql,qr = cdf[i], cdf[-1] - cdf[i]                    # CumSum of each division

        if ql == 0 or qr == 0:
            continue
    
        vl = calculateVariance(pl, wl, ql)                  # Variance of pl
        vr = calculateVariance(pr, wr, qr)                  # Variance of pr

        fn = (vl * ql) + (vr * qr)                          # Minimization function
        
        res.append((fn, i))

    return min(res, key = lambda t: t[0])[1]

#---------------------------------------------------------------------------------------------------

img = cv2.imread(args.filename)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

H,S,V = cv2.split(imgHSV)

# Run OTSU
cho = otsu(V)
ret,_ = cv2.threshold(V, 0, 255, cv2.THRESH_OTSU)

gen = apply(V, cho)
ref = apply(V, ret)

#cv2.imshow('Images', np.hstack((V, ref, gen)))

genHSV = np.dstack((H,S,gen))
genBGR = cv2.cvtColor(genHSV, cv2.COLOR_HSV2BGR)

# Combine to Image
refHSV = np.dstack((H,S,ref))
refBGR = cv2.cvtColor(refHSV, cv2.COLOR_HSV2BGR)

cv2.imshow('Correção na Região (Original, Gerado, Opencv)', np.hstack((img, genBGR, refBGR)))

while True:
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()
