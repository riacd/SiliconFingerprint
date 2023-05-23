import numpy as np

if __name__ == '__main__':
    rawData = np.load("UserEquipment/UE_feature_rawData/feature_clf1.npy")
    print(rawData.shape)
    print(rawData[0])