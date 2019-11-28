import math
import os
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

testfile = "/Users/fanbeishuang/fbs/workspace/py/PycharmProjects/godeyes/boxes_data_test.csv"


class BBoxesTool:
    _columns = ['x1', 'y1', 'x2', 'y2', 'score']
    _MaxPeoplePerTask = 120

    def __init__(self, boxes):
        self.boxes = pd.DataFrame(boxes, columns=self._columns)
        self._filter_outlier()
        self._to_location()

    def get_boxes(self):
        return self.boxes.values

    def get_boxes_loc(self):
        return

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

    def _filter_outlier(self):
        self.boxes['area'] = list(map(lambda x1, y1, x2, y2: (y2 - y1) * (x2 - x1),
                                      self.boxes['x1'], self.boxes['y1'], self.boxes['x2'], self.boxes['y2']))
        outliers = BBoxesTool.detect_outliers(self.boxes, 0, ['y1', 'area'])
        list_pridict_low = list(self.boxes.loc[self.boxes['score'] < np.percentile(self.boxes['score'], 15)].index)
        outliers = [val for val in outliers if val in list_pridict_low]
        # print(outliers)
        self.boxes = self.boxes.drop(outliers).drop(columns=['area'], axis=1)
        return

    def _gen_loc_parts(self, boxes):
        # boxes is sorted by x1
        # print(boxes.describe())
        sorted_y1 = boxes.sort_values(by=['y1'])
        print("=========sorted y1=============")
        # print(sorted_y1)
        raw_loc = {}  # raw_count[boxes_index]
        raw_count = 1
        for index, box in sorted_y1.iterrows():
            self.test_boxes = [index]
            return
            print("index:", index)
            if raw_count not in raw_loc:
                raw_loc[raw_count] = [index]
                continue
            cur_raw = raw_loc[raw_count]

            left_x = box.at['x1']
            w = (box.at['x2'] - left_x)
            left_x -= w
            right_x = left_x + 2 * w

            new_raw = False
            for rd_index in cur_raw:
                rd_box = boxes.loc[rd_index]
                x1 = rd_box.at['x1']
                x2 = rd_box.at['x2']
                if ((left_x > x1 and left_x < x2 ) or (right_x > x1 and right_x < x2)):
                    print("add raw")
                    new_raw = True
                    raw_count += 1
                    raw_loc[raw_count] = [index]
                    break
            if (not new_raw):
                raw_loc[raw_count].append(index)
            print ("raw_loc", raw_loc)
        return raw_loc

    def _to_location(self):
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
        # print(sorted_boxes)
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
            # return
            tasks.append(self._gen_loc_parts(sorted_boxes[begin:end]))
        # print(tasks)
        return tasks

    def get_test_boxes(self):
        # indexes = []
        # for index,_ in self.test_boxes.iterrows():
        #     indexes.append(index)
        return self.boxes.take(self.test_boxes).values

def gen_loc_of_test():
    boxes = pd.read_csv(testfile, header=0)
    # print(boxes.describe())
    btools = BBoxesTool(boxes)
    print("test boxes")
    # print(btools.get_boxes())
    print(btools.get_test_boxes())


#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', 500)
gen_loc_of_test()

