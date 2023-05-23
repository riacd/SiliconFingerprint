import numpy as np
import random
from fuzzyExtractor import FE
from converting import converting
from myPlot import nihe, two_nihe

def sameTest(inputfile, outputfile, deviceN, perRow, perTestN, my_t):
    rawData = np.load(inputfile)
    # theMax = rawData.max()
    # theMin = rawData.min()
    theMedian = np.median(rawData)
    fe = FE(511, my_t)
    out = open(outputfile, "a+")
    allPass = 0
    allCount = 0

    for i in range(deviceN):
        count = 0
        for t in range(perTestN):
            t1 = random.randint(1, perRow) - 1 + i * 200
            t2 = random.randint(1, perRow) - 1 + i * 200
            while t1 == t2:
                t2 = random.randint(1, perRow) - 1 + i * 200
            w1 = converting(rawData[t1], theMedian)
            w2 = converting(rawData[t2], theMedian)
            R1, s, x = fe.generate(w1)
            R2 = fe.reproduce(w2, s, x)

            allCount += 1
            if (R1 == R2).all():
                count += 1
                allPass += 1
                print("device {} test {} success!".format(i, t))
            else:
                print("device {} test {} fail...".format(i, t))
        # print("device {} success rate is {}\n".format(i, count / perTestN), file=out)
        print("device {} success rate is {}\n".format(i, count / perTestN))
    print("t is {} all success rate is {}\n".format(my_t, allPass / allCount),file=out)
    out.close()

def differTest(inputfile, outputfile2, deviceN, perRow, perTestN, my_t):
    rawData = np.load(inputfile)
    # theMax = rawData.max()
    # theMin = rawData.min()
    # 中位数
    theMedian = np.median(rawData)
    fe = FE(511, my_t)

    out2 = open(outputfile2, "a+")

    allCount = 0
    allPass = 0
    for i in range(deviceN):
        iCount = 0
        iPass = 0
        for j in range(deviceN):
            if j == i:
                continue
            # jCount = 0
            jPass = 0

            for t in range(perTestN):
                allCount += 1
                iCount += 1
                # jCount += 1
                t1 = random.randint(1, perRow) - 1 + i * 200
                t2 = random.randint(1, perRow) - 1 + j * 200
                #量化
                w1 = converting(rawData[t1], theMedian)
                w2 = converting(rawData[t2], theMedian)
                #模糊Gen
                R1, s, x = fe.generate(w1)
                #模糊Rep
                #Rep(w2, P)
                R2 = fe.reproduce(w2, s, x)
                if (R1 == R2).all():
                    print("device {} and device {} test {} pass!".format(i, j, t))
                    allPass += 1
                    iPass += 1
                    jPass += 1
                else:
                    print("device {} and device {} test {} unpass...".format(i, j, t))
            # print("device {} and device {} pass rate is {}\n".format(i,j, jPass/ perTestN), file=out1)
            print("device {} and device {} pass rate is {}\n".format(i,j, jPass/ perTestN))
        # print("device {} pass rate is {}\n".format(i, iPass / iCount), file=out2)
        print("device {} pass rate is {}\n".format(i, iPass / iCount))
    print("t is {} all pass rate is {}\n".format(my_t, allPass / allCount), file=out2)
    print("all pass rate is {}\n".format(allPass / allCount))
    out2.close()

def differBit(w1, w2):
    res = 0
    for i in range(len(w1)):
        if w1[i] != w2[i]:
            res += 1
    return res

def testRawData(inputfile, outputfile, deviceN, perRow, testN):
    rawData = np.load(inputfile)
    # theMax = rawData.max()
    # theMin = rawData.min()
    theMedian = np.median(rawData)
    out = open(outputfile, "a+")
    for i in range(deviceN):
        for j in range(deviceN):
            if i != j:
                continue
            count = 0
            num = 0
            for t in range(testN):
                t1 = random.randint(1, perRow) - 1 + i * 200
                t2 = random.randint(1, perRow) - 1 + j * 200
                while t1 == t2:
                    t2 = random.randint(1, perRow) - 1 + j * 200
                w1 = converting(rawData[t1], theMedian)
                w2 = converting(rawData[t2], theMedian)
                count += differBit(w1, w2)
                if differBit(w1, w2) <= 39:
                    num += 1
            print("device {} and device {} hamming distance is {} smaller than 39 is {}\n".format(i, j, count / testN, num/ testN), file=out)
            print("device {} and device {} hamming distance is {}\n".format(i, j, count / testN))
    out.close()


#测量一个设备内的汉明距离的平均值
def intraDistanceTest(inputfile,  outputfile, deviceN, perRow, testN):
    rawData = np.load(inputfile)
    # theMax = rawData.max()
    # theMin = rawData.min()
    #找中位数
    theMedian = np.median(rawData)
    out = open(outputfile, "a+")

    allCount = 0
    record = [0]*600
    for i in range(deviceN):
        print("now in device {}".format(i))
        count = 0
        D = 0
        for j in range(testN):
            t1 = random.randint(1, perRow) - 1 + i * perRow
            t2 = random.randint(1, perRow) - 1 + i* perRow
            while t1 == t2:
                t2 = random.randint(1, perRow) - 1 + i * perRow
           
            allCount += 1

            w1 = converting(rawData[t1], theMedian)
            w2 = converting(rawData[t2], theMedian)
            tmp = round(differBit(w1, w2) )
            record[int(tmp)] += 1
           
        # print("device {} hamming distance is {}\n".format(i, D/ count), file=out)
        # print("device {} hamming distance is {}\n".format(i, D/ count))

    for i in range(len(record)):
        print("Intra hamming distance {} is {}\n".format(i, record[i]/ allCount), file=out)
        print("Intra hamming distance {} is {}\n".format(i, record[i]/ allCount))
    
    for i in range(len(record)):
        record[i] /= allCount

    nihe(record,0)

    out.close()

#测量不同设备内的汉明距离的平均值
def interDistanceTest(inputfile,  outputfile, deviceN, perRow, testN):
    rawData = np.load(inputfile)
    # theMax = rawData.max()
    # theMin = rawData.min()
    theMedian = np.median(rawData)
    out = open(outputfile, "a+")

    allCount = 0
    record = [0]*600
    for i in range(deviceN):
        print("now in device {}".format(i))
        count = 0
        D = 0
        for j in range(testN):
            i2 = random.randint(1, 30) - 1
            while i2 == i:
                i2 = random.randint(1, 30) - 1
            t1 = random.randint(1, perRow) - 1 + i * perRow
            t2 = random.randint(1, perRow) - 1 + i2* perRow
           
            allCount += 1

            w1 = converting(rawData[t1], theMedian)
            w2 = converting(rawData[t2], theMedian)
            tmp = round(differBit(w1, w2) )
            record[int(tmp)] += 1
           
        # print("device {} hamming distance is {}\n".format(i, D/ count), file=out)
        # print("device {} hamming distance is {}\n".format(i, D/ count))

    for i in range(len(record)):
        print("Intra hamming distance {} is {}\n".format(i, record[i]/ allCount), file=out)
        print("Intra hamming distance {} is {}\n".format(i, record[i]/ allCount))
    
    for i in range(len(record)):
        record[i] /= allCount

    nihe(record,1)

    out.close()

#测量inter-distance和intra-distance并作图
def intraAndinterDistanceTest(inputfile,  outputfile, deviceN, perRow, testN):
    rawData = np.load(inputfile)
    # theMax = rawData.max()
    # theMin = rawData.min()
    theMedian = np.median(rawData)
    out = open(outputfile, "a+")

    allCount1 = 0
    allCount2 = 0
    record1 = [0]*600 #记录intradistance
    record2 = [0]*600 #interdistance

    for i in range(deviceN):
        print("now in device {}".format(i))
        for j in range(testN):
            t1 = random.randint(1, perRow) - 1 + i * perRow
            t2 = random.randint(1, perRow) - 1 + i* perRow
            while t1 == t2:
                t2 = random.randint(1, perRow) - 1 + i * perRow
           
            allCount1 += 1

            w1 = converting(rawData[t1], theMedian)
            w2 = converting(rawData[t2], theMedian)
            tmp = round(differBit(w1, w2) )
            record1[int(tmp)] += 1
        
        for j in range(testN):
            i2 = random.randint(1, 30) - 1
            while i2 == i:
                i2 = random.randint(1, 30) - 1
            t1 = random.randint(1, perRow) - 1 + i * perRow
            t2 = random.randint(1, perRow) - 1 + i2* perRow
           
            allCount2 += 1

            w1 = converting(rawData[t1], theMedian)
            w2 = converting(rawData[t2], theMedian)
            tmp = round(differBit(w1, w2) )
            record2[int(tmp)] += 1
           
        # print("device {} hamming distance is {}\n".format(i, D/ count), file=out)
        # print("device {} hamming distance is {}\n".format(i, D/ count))

    for i in range(len(record1)):
        print("Intra hamming distance {} is {}\n".format(i, record1[i]/ allCount1), file=out)
        print("Intra hamming distance {} is {}\n".format(i, record1[i]/ allCount1))
    
    for i in range(len(record2)):
        print("Inter hamming distance {} is {}\n".format(i, record2[i]/ allCount2), file=out)
        print("Inter hamming distance {} is {}\n".format(i, record2[i]/ allCount2))
    

    for i in range(len(record1)):
        record1[i] /= allCount1
        record2[i] /= allCount2
        record1[i] *= 10
        record2[i] *= 10

    two_nihe(record1, record2, True)
    
    
    out.close()




if __name__ == '__main__':
    intraAndinterDistanceTest("./rawData/feature_clf1.npy", "./globeCOM/interintra/res1",30, 200, 100000)
    # intraAndinterDistanceTest("./rawData/feature_clf2.npy", "./globeCOM/interintra/res1",30, 200, 100000)
    # intraAndinterDistanceTest("./rawData/feature_clf3.npy", "./globeCOM/interintra/res1",30, 200, 100000)
    # intraAndinterDistanceTest("./rawData/feature_clf4.npy", "./globeCOM/interintra/res1",30, 200, 100000)
    # intraAndinterDistanceTest("./rawData/feature_clf5.npy", "./globeCOM/interintra/res1",30, 200, 100000)
    # intraAndinterDistanceTest("./rawData/feature_clf6.npy", "./globeCOM/interintra/res1",30, 200, 100000)
    # interDistanceTest("./rawData/feature_clf1.npy", "./globeCOM/interDistance/res1",30, 200, 10000)
    # intraDistanceTest("./rawData/feature_clf2.npy", "./globeCOM/intraDistance/res2",30, 200, 10000)
    # intraDistanceTest("./rawData/feature_clf3.npy", "./globeCOM/intraDistance/res3",30, 200, 10000)
    # intraDistanceTest("./rawData/feature_clf4.npy", "./globeCOM/intraDistance/res4",30, 200, 10000)
    # intraDistanceTest("./rawData/feature_clf5.npy", "./globeCOM/intraDistance/res5",30, 200, 10000)
    # intraDistanceTest("./rawData/feature_clf6.npy", "./globeCOM/intraDistance/res6",30, 200, 10000)

    # t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 36, 37, 38, 39, 41, 42, 43, 45, 46, 47, 51, 53, 54, 55, 58, 59, 61, 62, 63, 85, 87, 91, 93, 95]
    

    # for i in t:
    #     if i > 40:
    #         sameTest("./rawData/feature_clf1.npy", "./sameRes/same", 30, 200, 40, i)
    #     else:
    #         sameTest("./rawData/feature_clf1.npy", "./sameRes/same", 30, 200, 90, i)
        

    # differTest("./rawData/feature_clf1.npy", "./differRes/differ", 30, 200, 3, 1)
   


    # testRawData("./rawData/feature_clf1.npy","./hamming/res2",30,200,1000)

    # rawData = np.load("./rawData/feature_clf2.npy")
    # theMedian = np.median(rawData)
    #
    # w1 = converting(rawData[0], theMedian)
    #
    # w2 = converting(rawData[400], theMedian)
    #
    # print(w1)
    # print(w2)
    # print(differBit(w1, w2))
    #
    # fe = FE(511, 4)
    # R1, s, x = fe.generate(w1)
    # R2 = fe.reproduce(w2, s, x)
    #
    # print(R1)
    # print(R2)
    # if (R1 == R2).all():
    #     print("ok")
    # else:
    #     print("fail")


