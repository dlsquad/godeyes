import face_recognition
import cv2
import json
import os


def write_dict_2_model(W, fullPath):
    """
    模型持久化
    :param W:
    :param fullPath:
    :return:
    """
    modelPath, modelName = os.path.split(fullPath)
    if modelPath != '':
        if not os.path.exists(modelPath):
            os.makedirs(modelPath)
    js_w = json.dumps(W, ensure_ascii=False)
    file = open(fullPath, 'w', encoding='utf-8')
    file.write(js_w)
    file.close()


def read_dict_model(fullPath):
    """
    模型加载
    :param fullPath:
    :return:
    """
    file = open(fullPath, 'r', encoding='utf-8')
    js_r = file.read()
    try:
        dic = json.loads(js_r)
    except Exception:
        print(fullPath)
    file.close()
    return dic


def drow_cv2_img(cv_arr):
    """
    绘制cv2图像
    :param cv_arr:
    :return:
    """
    cv2.namedWindow('draw', cv2.WINDOW_NORMAL)
    cv2.imshow('draw', cv_arr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_sim_face(img_name, known_encodings, topN=3):
    """
    判断新的图片是否在已有列表中
    :param img_name:目标人脸
    :param known_encodings:集体照中所有人脸的编码
    :return: 返回集体照中与目标人脸最相似的人脸索引
    """
    image_to_test = face_recognition.load_image_file(img_name)
    face_encodings = face_recognition.face_encodings(image_to_test, num_jitters=2)
    if len(face_encodings) <= 0:
        print('未找到该图片编码')
        return []
    image_to_test_encoding = face_encodings[0]
    face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)

    rs = sorted(enumerate(face_distances), key=lambda x: x[1])[0:topN]
    print('最相近的人脸topN:{}'.format(rs[0:topN]))
    return [i for i, j in rs]


def gnrt_know_encodings(image, ori_img):
    """
    获取编码
    :param image:
    :param ori_img:
    :return:
    """
    face_locations = face_recognition.face_locations(image)  # 识别
    print('该图像人脸个数：{}'.format(len(face_locations)))

    draw = image.copy()
    draw = draw[..., ::-1]
    known_encodings = []
    per_face_location = []
    for top, right, bottom, left in face_locations:
        per_face_location.append([top, right, bottom, left])
        sub_img = image[top - 3:bottom + 3, left - 3:right + 3]
        face_i = face_recognition.face_encodings(sub_img, num_jitters=1)
        if face_i:
            known_encodings.append(face_i[0].tolist())
        else:
            print('该脸编码异常：{}'.format((top, right, bottom, left)))
            cv2.rectangle(image, (left, top), (right, bottom), (255, 255, 0), 2)
            drow_cv2_img(image)
        draw = cv2.rectangle(draw, (left, top), (right, bottom), (255, 255, 0), 2)

    cv2.imwrite('{}_result.png'.format(ori_img.split('.')[0]), draw)
    return per_face_location, known_encodings


def get_face_locations(img_name):
    """
    若该图片人脸位置已经存在，则直接返回。否则重新计算
    :param img_name: 图片名字
    :return: 人脸位置 List((x1, y1, x2, y2, _))
    """
    model_name = '{}_face_locations.model'.format(img_name.split('.')[0])
    if not os.path.exists(model_name):
        arr_img = face_recognition.load_image_file(img_name)
        # 人脸位置
        ori_face_locations = face_recognition.face_locations(arr_img)
        ori_face_locations = [(left, top, right, bottom, 0) for top, right, bottom, left in ori_face_locations]
        write_dict_2_model(ori_face_locations, model_name)
    else:
        ori_face_locations = read_dict_model(model_name)
    return ori_face_locations


def get_face_encoding(img_name):
    """
    若该图片人脸编码已经存在，则直接返回。否则重新计算
    :param img_name: 图片名字
    :return: List(所有的人脸编码)
    """
    model_name = '{}_face_encodings.model'.format(img_name.split('.')[0])
    if not os.path.exists(model_name):
        arr_img = face_recognition.load_image_file(img_name)
        # 人脸编码
        ori_img_encodings = face_recognition.face_encodings(arr_img)
        write_dict_2_model([i.tolist() for i in ori_img_encodings], model_name)
    else:
        ori_img_encodings = read_dict_model(model_name)
    return ori_img_encodings


if __name__ == '__main__':
    group_photo_name = "mse.jpg"
    simFaceTopN = get_sim_face("../../static/picture/wangLei.jpg", get_face_encoding(group_photo_name))  # 寻找相似脸

    arr_img = face_recognition.load_image_file(group_photo_name)
    for i in simFaceTopN:
        x1, y1, x2, y2, _ = get_face_locations(group_photo_name)[i]
        draw2 = cv2.rectangle(arr_img, (x1, y1), (x2, y2), (255, 255, 0), 2)
        draw2 = draw2[..., ::-1]
        drow_cv2_img(draw2)
