import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="Name of the file", default="lena.jpg")
args = parser.parse_args()

#---------------------------------------------------------------------------------------------------

def equalization(img):
    hist,bins = np.histogram(img.flatten(), 256, [0,256])
    cdf = hist.cumsum()

    lookup = np.ma.masked_equal(cdf, 0)
    lookup = (lookup - lookup.min()) * 255 / (lookup.max() - lookup.min())
    lookup_norm = np.ma.filled(lookup, 0).astype('uint8')

    return lookup_norm[img]

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

V = equalization(V)

choice = otsu(V)
ret, opencv = cv2.threshold(V, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

V[V < choice] = 0
V[V >= choice] = 255

imgHSV = np.dstack((H,S,V))

cv2.imshow('Original', np.hstack((img,imgHSV)))
cv2.imshow('Otsu Method (Code, Opencv)', np.hstack((V, opencv)))

cv2.waitKey(0)
cv2.destroyAllWindows()
