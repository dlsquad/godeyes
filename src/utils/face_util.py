import os
import cv2
import json
import typing
import logging
import asyncio
import aiofiles
import aioredis
import aiomysql
import face_recognition
from aiofiles import os as async_os

from .gen_loc import BBoxesTool


BTOOL_DICT = {}

logger = logging.getLogger("web")


class FaceUtil:

    model_path = "./model"

    def __init__(self, target_path: str, group_path: str):
        """
        Args:
            target_path (PATH): 需要识别的人像路径
            group_path (PATH): 合照路径
        """
        self.target_path = target_path
        self.group_path = group_path
        self.timg = face_recognition.load_image_file(target_path)
        self.gimg = face_recognition.load_image_file(group_path)

    async def __call__(self, fpath: str) -> (int, int):
        """ 在合照中框出目标用户，并保存成文件到指定路径。
        Args:
            fpath (PATH): 文件路径
        Return:
            position x: 用户所在排
            position y: 用户所在列
        """
        code = self.group_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        encoding_path = f"{self.model_path}/{code}-encode.model"
        location_path = f"{self.model_path}/{code}-location.model"
        if not (os.path.exists(location_path) and os.path.exists(encoding_path)
            and (await async_os.stat(location_path)).st_size > 0
            and (await async_os.stat(encoding_path)).st_size > 0):
            return f"picture:{code} is under preprocessing, please wait seconds."

        await asyncio.gather(
            self._load_location(location_path),
            self._load_encoding(encoding_path)
        )
        if code in BTOOL_DICT:
            self.btool = BTOOL_DICT.get(code)
        else:
            self.btool = BBoxesTool([list(l)+[0] for l in self.group_location])
            BTOOL_DICT.update({code: self.btool})

        indexes = self._get_similar_face_indexes()
        if not indexes:
            return f"there is no face in users photo."
        location = self.group_location[indexes[0]]
        self._draw_box_and_save(fpath, location)
        return self.btool.get_boxi_loc(indexes[0])

    def _draw_box_and_save(self, fpath: str, location: typing.Tuple[int]):
        draw_image = self.gimg.copy()
        top, right, bottom, left = location
        draw_image = cv2.rectangle(draw_image, 
            (left, top), (right, bottom), (255, 255, 0), 2)
        cv2.imwrite(fpath, draw_image[..., ::-1])

    async def _load_encoding(self, fpath: str):
        """从文件中载入人脸编码"""
        async with aiofiles.open(fpath, "r") as f:
            self.group_encoding = json.loads(await f.read())

    async def _load_location(self, fpath: str):
        """从文件中载入人脸位置"""
        async with aiofiles.open(fpath, "r") as f:
            self.group_location = json.loads(await f.read())

    def _get_similar_face_indexes(self, k: int=1) -> typing.List[int]:
        """ 获取最相似的k个人脸位置"""
        target_encoding = face_recognition.face_encodings(self.timg)
        if not target_encoding:
            return []
        distances = face_recognition.face_distance(target_encoding[0], self.group_encoding)
        return [i for i, _ in sorted(enumerate(distances), key=lambda x: x[1])[0:k]]

    @classmethod
    async def get_table_info(cls, code: str) -> typing.Dict[int, int]:
        if code in BTOOL_DICT:
            return BTOOL_DICT.get(code).get_boxes_info().to_dict()

        location_path = f"{cls.model_path}/{code}-location.model"
        if not (os.path.exists(location_path) and (
            await async_os.stat(location_path)).st_size > 0):
            return None

        async with aiofiles.open(location_path, "r") as f:
            group_location = json.loads(await f.read())
        btool = BBoxesTool([list(l)+[0] for l in group_location])
        BTOOL_DICT.update({code: btool})
        return btool.get_boxes_info().to_dict()

