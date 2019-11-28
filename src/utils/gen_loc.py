import math
import os
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

testfile = "/home/fbs/fbs/workspace/PycharmProjects/face_detection/mxnet_mtcnn_face_detection/boxes_data_test.csv"


class BBoxesTool:
    _columns = ['x1', 'y1', 'x2', 'y2', 'score']
    _MaxPeoplePerTask = 30

    def __init__(self, boxes):
        self.boxes = pd.DataFrame(boxes, columns=self._columns)

    def detect_outliers(df, n, features):
        """
        Tuckey算法
        """
        outlier_indices = []

        # iterate over features(columns)
        for col in features:
            # 1st quartile (25%)
            Q1 = np.percentile(df[col], 25)
            # 3rd quartile (75%)
            Q3 = np.percentile(df[col], 75)
            # Interquartile range (IQR)
            IQR = Q3 - Q1

            # outlier step
            outlier_step = 1.5 * IQR
            # Determine a list of indices of outliers for feature col
            outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step)].index

            # append the found outlier indices for col to the list of outlier indices
            outlier_indices.extend(outlier_list_col)

        # select observations containing more than 2 outliers
        outlier_indices = Counter(outlier_indices)
        multiple_outliers = list(k for k, v in outlier_indices.items() if v > n)
        return multiple_outliers

    def filter_outlier(self):
        self.boxes['area'] = list(map(lambda x1, y1, x2, y2: (y2 - y1) * (x2 - x1),
                                      self.boxes['x1'], self.boxes['y1'], self.boxes['x2'], self.boxes['y2']))
        outliers = BBoxesTool.detect_outliers(self.boxes, 0, ['y1', 'area'])
        list_pridict_low = list(self.boxes.loc[self.boxes['score'] < np.percentile(self.boxes['score'], 15)].index)
        outliers = [val for val in outliers if val in list_pridict_low]
        print(outliers)
        self.boxes = self.boxes.drop(outliers).drop(columns=['area'], axis=1)
        return

    def gen_loc_parts(boxes):
        # boxes is sorted by x1
        print(boxes)
        locs=[]
        for i in boxes:
            boxes
        return

    def box_to_location(self):
        """
            gen location from boxes location
        Parameters:
        ----------
            bboxes: numpy array, n x 5 (x1,y2,x2,y2,score)
        Retures:
        -------
            peaple location: DataFrame (index: raw, col, bbox_index)
        """
        sorted_boxes = pd.DataFrame(self.boxes, columns=self._columns).sort_values(by=['x1'])
        print(sorted_boxes)
        people_num = len(sorted_boxes)
        # minX = sorted_boxes['x1'].min()
        # minY = pdBoxes['y1'].min()
        # maxX = sorted_boxes['x2'].max()
        # maxY = pdBoxes['y2'].max()
        task_num = 1
        # stepWidth = 0
        if people_num / self._MaxPeoplePerTask > 2:
            task_num = math.ceil(float(people_num) / float(self._MaxPeoplePerTask))
            # stepWidth = math.ceil(float(maxX - minX) / float(task_num))
        # split tasks
        tasks = []
        for i in range(task_num):
            begin = i * self._MaxPeoplePerTask
            end = (i + 1) * self._MaxPeoplePerTask
            if end > people_num:
                end = people_num
            # print(begin , end)
            tasks.append(BBoxesTool.gen_loc_parts(sorted_boxes[begin:end]))
        print(tasks)
        return tasks


def gen_loc_of_test():
    boxes = pd.read_csv(testfile, header=0)
    # print(boxes.describe())
    btools = BBoxesTool(boxes)
    btools.filter_outlier()
    return btools.box_to_location()


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 500)
gen_loc_of_test()

