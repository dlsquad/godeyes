import os
import cv2
import json
import typing

import aiofiles
import face_recognition

from .gen_loc import BBoxesTool


class FaceUtil:

    model_path = "./model"

    def __init__(self, target_path: str, group_path: str):
        """
        Args:
            target_path (PATH): 需要识别的人像路径
            group_path (PATH): 合照路径
        """
        self.timg = face_recognition.load_image_file(target_path)
        self.gimg = face_recognition.load_image_file(group_path)

    async def __aenter__(self):
        """进入上下文，若合照人脸编码已经存在则从
        文件中载入，若不存在则生成之后保存到文件中。
        """
        code = self.group_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        encoding_path = f"{self.model_path}/{code}-encode.model"
        location_path = f"{self.model_path}/{code}-location.model"
        if os.path.exists(location_path):
            await self._load_location(location_path)
        else:
            await self._save_location(location_path)

        if os.path.exists(encoding_path):
            await self._load_encoding(encoding_path)
        else:
            await self._save_encoding(encoding_path)

        self.target_encoding = face_recognition.face_encodings(self.timg)[0]

    async def __call__(self, fpath) -> (int, int):
        """ 在合照中框出目标用户，并保存成文件到指定路径。
        Args:
            fpath (PATH): 文件路径
        Return:
            position x: 用户所在排
            position y: 用户所在列
        """
        async with self:
            index = self._get_similar_faces()[0]
            location = self.group_location[index]
            position = self.btool.get_boxi_loc(index)
            self._draw_box_and_save(fpath, location)

    def _draw_box_and_save(fpath: str, location: typing.Tuple):
        draw_image = self.gimg.copy()
        top, right, bottom, left = location
        draw_image = cv2.rectangle(self.gimg, (left, top), (right, bottom), (255, 255, 0), 2))
        cv2.imwrite(fpath, draw_image)

    async def _save_encoding(self, fpath: str):
        """获取人脸编码，保存到文件"""
        async with aiofiles.open(fpath, "w") as f:
            self.group_encoding = face_recognition.face_encodings(self.gimg, 
                                                            self.group_location)
            await f.write(json.dumps([e.tolist() for e in self.group_encoding]))

    async def _load_encoding(self, fpath: str):
        """从文件中载入人脸编码"""
        async with aiofiles.open(fpath, "r") as f:
            self.group_encoding = json.loads(await f.read())

    async def _save_location(self, fpath: str):
        """获取人脸位置并保存到文件"""
        async with aiofiles.open(fpath, "w") as f:
            self.group_location = face_recognition.face_locations(self.gimg)
            self.btool = BBoxesTool([list(l)+[0] for l in self.group_location])
            await f.write(json.dumps(self.group_location))

    async def _load_location(self, fpath: str):
        """从文件中载入人脸位置"""
        async with aiofiles.open(fpath, "r") as f:
            self.group_location = json.loads(await f.read())
            self.btool = BBoxesTool([list(l)+[0] for l in self.group_location])

    def _get_similar_faces(self, k: int=1):
        """ 获取最相似的k个人脸位置"""
        face_distance = face_recognition.face_distance(self.target_encoding,
                                                       self.group_encoding)
        return [for i, _ in sorted(enumerate(face_distances, lambda x: x[1]))[0:k]]
