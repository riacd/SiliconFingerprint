from feTest import differTest
t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 36, 37, 38, 39, 41, 42, 43, 45, 46, 47, 51, 53, 54, 55, 58, 59, 61, 62, 63, 85, 87, 91, 93, 95]
    

for i in t:
    if i > 40:
        differTest("./rawData/feature_clf1.npy", "./differRes/differ", 30, 200, 2, i)
    else:
        differTest("./rawData/feature_clf1.npy", "./differRes/differ", 30, 200, 3, i)