import os
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

columns=['x1','y1','x2','y2','score']
testfile="/home/fbs/fbs/workspace/PycharmProjects/face_detection/mxnet_mtcnn_face_detection/boxes_data_test.csv"
N = 5

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

def filter_outlier(bboxes):
    pdBoxes = pd.DataFrame(bboxes, columns=columns)
    pdBoxes['area'] = list(map(lambda x1,y1,x2,y2: (y2-y1)*(x2-x1), pdBoxes['x1'],pdBoxes['y1'],pdBoxes['x2'], pdBoxes['y2']))
    # print(pdBoxes.describe())
    # plt.hist(pdBoxes['area'])
    # plt.show()
    # pdBoxes.to_csv(testfile,columns=['x1','y1','x2','y2','score'],index=False)
    outliers = detect_outliers(pdBoxes,0,['y1','area'])
    listPridictLow = list(pdBoxes.loc[pdBoxes['score'] < np.percentile(pdBoxes['score'], 15)].index)
    outliers = [val for val in outliers if val in listPridictLow]
    print(outliers)
    pdBoxes = pdBoxes.drop(outliers).drop(columns=['area'],axis=1)
    # pdBoxes = pdBoxes.take(outliers)
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
    hdf = pd.DataFrame(bboxes,columns=columns).sort_values(by=['x1'])
    print(hdf)
    peopleNum = len(hdf)
    minX = hdf['x1'].min()
    minY = hdf['y1'].min()
    maxX = hdf['x2'].max()
    maxY = hdf['y2'].max()
    step = 1
    stepWidth = 0
    if (peopleNum / N > 10 ):
        step = peopleNum / N
        stepWidth = (maxX - minX) / N
    return hdf

def GenLocOfTest():
    boxes = pd.read_csv(testfile,header=0)
    # print(boxes.describe())
    print(box_to_location(filter_outlier(boxes)))
    return


pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth',500)

GenLocOfTest()
