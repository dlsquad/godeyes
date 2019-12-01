import os
import cv2
import json
import typing

import aiofiles
import face_recognition


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
        if os.path.exists(encoding_path):
            await self._load_encoding(encoding_path)
        else:
            await self._save_encoding(encoding_path)
        if os.path.exists(location_path):
            await self._load_location(location_path)
        else:
            await self._save_location(location_path)
        self.group_encoding = face_recognition.face_encodings(self.timg)

    async def __call__(self, fpath) -> (int, int):
        """ 在合照中框出目标用户，并保存成文件到指定路径。
        Args:
            fpath (PATH): 文件路径
        Return:
            position x: 用户所在排
            position y: 用户所在列
        """
        async with self, aiofiles.open(fpath, "wb") as f:
            pass

    async def _save_encoding(self, fpath: str):
        """获取人脸编码，保存到文件"""
        async with aiofiles.open(fpath, "w") as f:
            self.group_encoding = face_recognition.face_encodings(self.gimg)
            await f.write(json.dumps([e.tolist() for e in self.group_encoding]))

    async def _load_encoding(self, fpath: str):
        """从文件中载入人脸编码"""
        async with aiofiles.open(fpath, "r") as f:
            self.group_encoding = json.loads(await f.read())

    async def _save_location(self, fpath: str):
        """获取人脸位置并保存到文件"""
        async with aiofiles.open(fpath, "w") as f:
            self.group_location = face_recognition.face_locations(self.gimg)
            await f.write(json.dumps(self.group_location))

    async def _load_location(self, fpath: str):
        """从文件中载入人脸位置"""
        async with aiofiles.open(fpath, "r") as f:
            self.group_location = json.loads(await f.read())

    def _draw_box(self):
        pass

    def _get_similar_faces(self, k: int=1):
        """ 获取最相似的k个人脸位置"""
        face_distance = face_recognition.face_distance(self.target_encoding,
                                                       self.group_encoding)
        # return [f[0] for f in sorted(face_distance, key=lambda x:x[1])[0:k]]
