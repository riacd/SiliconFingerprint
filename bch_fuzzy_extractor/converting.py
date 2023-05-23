import numpy as np


def converting(data, theMedian):
    res = ''
    for i in data:
        if i > theMedian:
            res += '1'
        else:
            res += '0'
    return res

if __name__=="__main__":
    rawData = np.load("./rawData/feature_clf1.npy")
    theMax = rawData.max()
    theMin = rawData.min()
    theMedian = np.median(rawData)

    print(theMin, theMax, theMedian)

    print( converting(rawData[5999], theMedian) )