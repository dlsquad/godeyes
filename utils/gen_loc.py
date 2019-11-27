import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

testfile="/Users/fanbeishuang/fbs/workspace/py/PycharmProjects/godeyes/boxes_data_test.csv"
def detect_outliers(df,n,features):
    """
    Tuckey算法
    """
    outlier_indices = []

    # iterate over features(columns)
    for col in features:
        # 1st quartile (25%)
        Q1 = np.percentile(df[col], 25)
        # 3rd quartile (75%)
        Q3 = np.percentile(df[col],75)
        # Interquartile range (IQR)
        IQR = Q3 - Q1

        # outlier step
        outlier_step = 1.5 * IQR

        # Determine a list of indices of outliers for feature col
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step )].index

        # append the found outlier indices for col to the list of outlier indices
        outlier_indices.extend(outlier_list_col)

    # select observations containing more than 2 outliers
    outlier_indices = Counter(outlier_indices)
    multiple_outliers = list( k for k, v in outlier_indices.items() if v > n )
    return multiple_outliers

def fillter_outlier(bboxes):
    pdBoxes = pd.DataFrame(bboxes, columns=['x1','y1','x2','y2','score'])
    # pdBoxes.to_csv(testfile,columns=['x1','y1','x2','y2','score'],index=False)
    outliers = detect_outliers(pdBoxes,0,['y1'])
    pdBoxes = pdBoxes.drop(outliers)
    # print(pdBoxes.describe())
    return pdBoxes.values

def box_to_location(bboxes):
    """
        gen location from boxes location
    Parameters:
    ----------
        bboxes: numpy array, n x 5 (x1,y2,x2,y2,score)
    Retures:
    -------
        peaple location: DataFrame (index: raw, col, bbox_index)
    """
    hdf = pd.DataFrame(bboxes)
    return hdf

def testGenLoc():
    boxes = pd.read_csv(testfile,header=0)
    # print(boxes.describe())
    fillter_outlier(boxes)
    return


# testGenLoc()