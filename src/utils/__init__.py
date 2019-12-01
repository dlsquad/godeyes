import os
import base64
import random


def gen_code() -> str:
    """生成6位数字的验证码"""
    return "".join(str(i) for i in random.choices(range(0, 9), k=6))


def get_file_in_path(path: str, fname: str) -> str:
    """ 从目标路径中获取文件
    Args:
        path (String): 目标路径
        fname (String): 没有后缀名的文件名
    return: 文件名
    """
    for f in os.listdir(path):
        if fname == f.rsplit(".", 1)[0]:
            return f
    return ""

