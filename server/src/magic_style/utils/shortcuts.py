import json
import datetime
import logging
import os
import random

from collections import OrderedDict

import numpy as np
import cv2
from django.utils import timezone
from django.conf import settings
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        if isinstance(o, OrderedDict):
            return dict(o)
        if isinstance(o, datetime.datetime):
            return datetime_pretty(o)
        return json.JSONEncoder.default(self, o)


def datetime_pretty(value=None, *, fmt="%Y-%m-%d %H:%M:%S %Z"):
    """
    :param fmt: 返回时间格式
    :param value: 时间，如果是 None 就返回当前时间
    """
    return timezone.localtime(value, timezone=settings.TIME_ZONE).strftime(fmt)


def rand_str(length=32, type="lower_hex"):
    """
    生成指定长度的随机字符串或者数字, 可以用于密钥等安全场景
    :param length: 字符串或者数字的长度
    :param type: str 代表随机字符串，num 代表随机数字
    :return: 字符串
    """
    if type == "str":
        return get_random_string(length, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    elif type == "lower_str":
        return get_random_string(length, allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789")
    elif type == "lower_hex":
        return random.choice("123456789abcdef") + get_random_string(length - 1, allowed_chars="0123456789abcdef")
    elif type == "letter":
        return get_random_string(length, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    else:
        return random.choice("123456789") + get_random_string(length - 1, allowed_chars="0123456789")


def create_random_image(image_name, image_path=settings.STYLE_IMAGE_PATH):
    filename = os.path.join(image_path, image_name)
    img = np.zeros([400, 400, 3], np.uint8)
    cv2.imwrite(filename, img)


def save_file(file, filename, path=settings.DOWNLOAD_DIR):
    if not (os.path.exists(path) and os.path.isdir(path)):
        os.mkdir(path)

    file_path = os.path.join(path, filename)
    with open(file_path, 'wb+') as fp:
        for chunks in file.chunks():
            fp.write(chunks)


def delete_file(filename, path=settings.DOWNLOAD_DIR):
    file_path = os.path.join(path, filename)
    os.remove(file_path)


def copy_file(from_filename, to_filename, from_path=settings.DOWNLOAD_DIR, to_path=settings.DOWNLOAD_DIR):
    with open(os.path.join(to_path, to_filename), 'wb') as f:
        with open(os.path.join(from_path, from_filename), 'rb') as fp:
            f.write(fp.read())
