# coding: utf-8
import mxnet as mx
import numpy as np
from mtcnn_detector import MtcnnDetector
import cv2

import os
import time

# import datetime
# starttime = datetime.datetime.now()
from src.utils.gen_loc import BBoxesTool

detector = MtcnnDetector(model_folder='model', ctx=mx.cpu(0), num_worker = 4 , accurate_landmark = False)

img = cv2.imread('2019MSEtest.jpeg')
w, h = img.shape[0:2]
# draw = np.zeros((w,h),np.uint8)#生成一个空灰度图像

# run detector
results = detector.detect_face(img)
if results is not None:
    bboxes = BBoxesTool(results[0])
    bboxes.filter_outlier()
    total_boxes=bboxes.boxes.values
    points = results[1]

    # print(total_boxes)
    # extract aligned face chips
    # chips = detector.extract_image_chips(img, points, 144, 0.37)
    # for i, chip in enumerate(chips):
    #     cv2.imshow('chip_'+str(i), chip)
    #     cv2.imwrite('chip_'+str(i)+'.png', chip)

    draw = img.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i, b in enumerate(total_boxes):
        cv2.rectangle(draw, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (255, 0, 255), thickness=5)
        # cv2.putText(draw, str(i), (int(b[0]), int(b[1])), font, fontScale=2, color=(255, 0, 255), thickness=3)

    # for p in points:
    #     for i in range(5):
    #         cv2.circle(draw, (p[i], p[i + 5]), 1, (0, 0, 255), 2)

    draw = cv2.resize(draw, (int(h / 3), int(w / 3)))

    # print("Time used:", (datetime.datetime.now() - starttime))
    cv2.imshow("detection result", draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# --------------
# test on camera
# --------------
'''
camera = cv2.VideoCapture(0)
while True:
    grab, frame = camera.read()
    img = cv2.resize(frame, (320,180))
    t1 = time.time()
    results = detector.detect_face(img)
    print 'time: ',time.time() - t1
    if results is None:
        continue
    total_boxes = results[0]
    points = results[1]
    draw = img.copy()
    for b in total_boxes:
        cv2.rectangle(draw, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (255, 255, 255))
    for p in points:
        for i in range(5):
            cv2.circle(draw, (p[i], p[i + 5]), 1, (255, 0, 0), 2)
    cv2.imshow("detection result", draw)
    cv2.waitKey(30)
'''
