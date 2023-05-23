
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

def smooth_xy(x, y):
    """数据平滑处理

    :param lx: x轴数据，数组
    :param ly: y轴数据，数组
    :return: 平滑后的x、y轴数据，数组 [slx, sly]
    """
    # x = np.array(lx)
    # y = np.array(ly)
    x_smooth = np.linspace(x.min(), x.max(), 300)
    y_smooth = make_interp_spline(x, y)(x_smooth)
    return x_smooth, y_smooth


def nihe(nums, decide = False):
    if len(nums) > 512:
        nums = nums[:512]
    x=np.arange(0,len(nums) ,1) #生成散点列表作为x的值
    y=np.array(nums) #给定y的散点值

    #1的话进行平滑处理
    if decide == 1:
        x, y = smooth_xy(x, y)

    plt.plot(x,y,label='original values')

    # plt.scatter(x, y, s=5)
    plt.xlabel('X ')
    plt.ylabel('Y')

    plt.legend(loc=3) #设置图示的位置
    # plt.title('polyfitting') #设置标题
    plt.show() #显示图片

def two_nihe(nums1, nums2, decide = False):
    if len(nums1) > 511:
        nums1 = nums1[:511]
    x1=np.arange(0,len(nums1) ,1) #生成散点列表作为x的值
    y1=np.array(nums1) #给定y的散点值

    if len(nums2) > 511:
        nums2= nums2[:511]
    x2=np.arange(0,len(nums2) ,1) #生成散点列表作为x的值
    y2=np.array(nums2) #给定y的散点值


    #1的话进行平滑处理
    if decide == True:
        x1, y1 = smooth_xy(x1, y1)
        x2, y2 = smooth_xy(x2, y2)

    plt.plot(x1 , y1, label = 'Intra-distance', linewidth=2.5)
    plt.plot(x2 , y2, label = 'Inter-distance', linewidth=2.5, linestyle = 'dotted')

    # plt.scatter(x, y, s=5)
    plt.xlabel('Hamming Distance',fontsize = 13)
    # plt.ylabel('Probability')

    # plt.legend(loc=3) #设置图示的位置
    
    plt.rcParams.update({'font.size': 13})
    plt.xticks(fontproperties = 'Times New Roman', size = 13)
    plt.yticks(fontproperties = 'Times New Roman', size = 13)
    plt.legend(loc='upper right')
    # plt.title('Intra-distance and inter-distance') #设置标题
    plt.show() #显示图片

def tPlot(decide):
    num_x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 36, 37, 38, 39, 41, 42, 43, 45, 46, 47, 51, 53, 54, 55, 58, 59, 61, 62, 63, 85, 87, 91, 93, 95]
    num_y = [0.00037037037037037035,0.0011111111111111111,0.0022222222222222222,0.008148148148148147,0.01037037037037037, 0.014074074074074074,0.015555555555555555, 0.026296296296296297,0.03777777777777778,0.04888888888888889,0.06333333333333334, 0.07481481481481482,0.09074074074074075,0.11,0.12333333333333334,0.16333333333333333,0.17407407407407408,0.19444444444444445,0.20333333333333334,0.24444444444444444,0.24925925925925925, 0.2607407407407407,0.3174074074074074,0.31925925925925924,0.33185185185185184,0.3411111111111111, 0.37666666666666665, 0.3888888888888889,0.412962962962963, 0.4825925925925926, 0.49333333333333335,0.5044444444444445, 0.5196296296296297,0.5683333333333334,0.5766666666666667,0.5858333333333333, 0.6008333333333333, 0.615,  0.620, 0.6366666666666667, 0.66, 0.67333333, 0.68, 0.7083333333333334,  0.7133333333333334,  0.7233333333333334, 0.7291666666666666,0.7383333333333334,0.7833333333333333,0.79, 0.8025,0.8033333333333333,0.805] 
    num_z = [0,0,0,0,0,0,0,0,0,0,0,0.0007662835249042146,0.0007662835249042146,0.0011494252873563218, 0.0015325670498084292,0.0026819923371647508,0.0026819923371647508,0.0030651340996168583,0.0034482758620689655,0.0038314176245210726,0.0038314176245210726,0.00421455938697318,0.005747126436781609, 0.006513409961685823,0.006130268199233717,0.0072796934865900385, 0.008045977011494253,0.009578544061302681,0.010727969348659003, 0.010727969348659003, 0.01264367816091954, 0.014176245210727969, 0.014942528735632184,  0.017241379310344827,0.01839080459770115,  0.01839080459770115,  0.01896551724137931,0.023563218390804597,0.023563218390804597,0.026436781609195402,0.029885057471264367,0.03218390804597701,0.0339080459770115, 0.039655172413793106,0.040229885057471264,0.04310344827586207, 0.04310344827586207, 0.04942528735632184,  0.10057471264367816, 0.10229885057471265, 0.10919540229885058, 0.11609195402298851,  0.12126436781609196]

    x=np.array(num_x) #生成散点列表作为x的值
    y=np.array(num_y) #给定y的散点值
    z = np.array(num_z)
    #1的话进行平滑处理

    x1, x2 = x, x
    if decide == True:
        x1, y = smooth_xy(x, y)
        x2, z = smooth_xy(x, z)

    # plt.figure(figsize=(5, 4))
    plt.plot(x1,y,label='GAR' , linewidth=2.5, color = 'g')
    plt.plot(x2,z,label='FAR',  linewidth=2.5, linestyle = 'dashed', color = 'firebrick')

    # plt.scatter(x, y, s=5)
    plt.xlabel('Error-correcting capability t',fontsize = 13)
    # plt.ylabel('Y')
    

    plt.rcParams.update({'font.size': 13})
    plt.xticks(fontproperties = 'Times New Roman', size = 13)
    plt.yticks(fontproperties = 'Times New Roman', size = 13)
    plt.legend(loc='upper left')
    # plt.title('polyfitting') #设置标题
    plt.show() #显示图片
    # plt.savefig("GAR_FAR.pdf")

if __name__ == "__main__":
    # nihe( [1,2,3,4,5,6,7,8,8,9,90,0,7,8,8], 0)
    #two_nihe([1,2,3,4,5,6,7,8,8,9,90,0,7,8,8],[2,32,34,32,3,2,3,4], True)
    tPlot(True)