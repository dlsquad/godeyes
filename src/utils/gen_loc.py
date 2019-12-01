import math
import os
import sys

import pandas as pd
import numpy as np
from collections import Counter


class BBoxesTool:

    _columns = ['x1', 'y1', 'x2', 'y2', 'score']
    _columns_rc = ['raw', 'col']
    _MaxPeoplePerTask = 120

    def __init__(self, boxes, outlier_check=False):
        self.boxes = pd.DataFrame(boxes, columns=self._columns)
        if outlier_check:
            self._filter_outlier()
        self._to_location()

    def get_boxes(self):
        return self.boxes[self._columns].values

    def get_boxi_loc(self, index):
        return [self.boxes.loc[index].at['raw'], self.boxes.loc[index].at['col']]

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
        # self.boxes.to_csv(testfile,columns=['x1','y1','x2','y2','score'],index=False)

        self.boxes['area'] = list(map(lambda x1, y1, x2, y2: (y2 - y1) * (x2 - x1),
                                      self.boxes['x1'], self.boxes['y1'], self.boxes['x2'], self.boxes['y2']))
        outliers = BBoxesTool.detect_outliers(self.boxes, 0, ['y1', 'area'])
        list_pridict_low = list(self.boxes.loc[self.boxes['score'] < np.percentile(self.boxes['score'], 15)].index)
        outliers = [val for val in outliers if val in list_pridict_low]
        # print(outliers)
        self.boxes = self.boxes.drop(outliers).drop(columns=['area'], axis=1)

    def _gen_loc_parts(self, boxes):
        sorted_y1 = boxes.sort_values(by=['y1'], ascending=False)
        # print(sorted_y1)
        raw_loc = {}  # raw_count[boxes_index]
        raw_count = 1
        for index, box in sorted_y1.iterrows():
            if raw_count not in raw_loc:
                raw_loc[raw_count] = [index]
                continue

            left_x = box.at['x1']
            w = (box.at['x2'] - left_x)/2
            left_x -= w
            right_x = left_x + 2 * w

            new_raw = False
            for rd_index in raw_loc[raw_count]:
                rd_box = boxes.loc[rd_index]
                x1 = rd_box.at['x1']
                x2 = rd_box.at['x2']
                # print("rd_index:", rd_index, ",x1:", x1, ",x2:", x2, ",left_x:", left_x, ",right_x:", right_x)
                if (x1 <= left_x <= x2) or (left_x <= x1 and right_x >= x2) or (x1 <= right_x <= x2):
                    new_raw = True
                    # if raw_count == 4:
                    #     self.test_boxes = raw_loc[raw_count]
                    #     return raw_loc
                    raw_count += 1
                    raw_loc[raw_count] = [index]
                    break
            if not new_raw:
                raw_loc[raw_count].append(index)

        self.test_boxes = raw_loc[raw_count]
        return raw_loc

    def _raw_loc_to_box_info(self, raw_loc):
        # resorted boxes
        raw_col_info = []
        for raw, indexes in raw_loc.items():
            col_count = 0
            raw_boxes = self.boxes.take(indexes).sort_values(by=['x1'])
            for index, box in raw_boxes.iterrows():
                col_count += 1
                raw_col_info.append([index, raw, col_count])
                # print(raw_col_info)

        raw_col_pd = pd.DataFrame(raw_col_info, columns=['ind','raw', 'col']).sort_values(by='ind') #.drop('index', axis=1)
        # raw_col_pd = raw_col_pd.drop(columns=['ind'], axis=1)
        self.boxes['raw'] = list(raw_col_pd['raw'])
        self.boxes['col'] = list(raw_col_pd['col'])
        return

    def get_boxes_info(self):
        return self.boxes.groupby('raw')['col'].count()

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
        task_num = 1
        # stepWidth = 0
        if people_num / self._MaxPeoplePerTask > 2:
            task_num = math.ceil(float(people_num) / float(self._MaxPeoplePerTask))
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
        return self._raw_loc_to_box_info(self._merge_gen_loc_tasks(tasks))

    def _merge_gen_loc_tasks(self, tasks):
        res = {}
        for loc_map in tasks:
            for raw, indexes in loc_map.items():
                if raw not in res:
                    res[raw] = indexes
                    continue
                res[raw].extend(indexes)
        return res

    def get_test_boxes(self):
        # indexes = []
        # for index,_ in self.test_boxes.iterrows():
        #     indexes.append(index)
        return self.boxes.take(self.test_boxes).values


if __name__ == "__main__":
    import face_recognition
    fpath = "../../static/picture/123456.jpg"
    face_encodings = face_recognition.load_image_file(fpath)
    face_locations = face_recognition.face_location(face_encodings)

    btools = BBoxesTool(face_locations)
    btools = BBoxesTool(boxes)
    print(btools.get_boxes_info())
    print(btools.get_boxi_loc(6))
    print(btools.get_boxi_loc(66))

