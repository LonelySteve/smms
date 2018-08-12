import os
import random
import re
import string
import time
from io import BytesIO

import requests
from PIL import Image
from requests_toolbelt import MultipartEncoder

import smms.exceptions as exceptions
import smms.upload_result as upload_result


class Uploader(object):

    def __init__(self, img_fp, img_name=None):
        """实例化一个图片上传器。优先使用指定的图片名，如果未指定，
        那么将会尝试从传入的路径、地址或file-like Object中提取图
        片名，失败则默认以‘Unknown’为主文件名，扩展名则由图片类型
        自动决定。将自动判断传入的图片的类型。

        :param img_fp: 图片的磁盘路径，或基于HTTP及HTTPS协议的图片超链接，或file-like Object
        :type img_fp: str,file-like Object
        :param img_name: 图片的主文件名，默认为 None
        :param img_name: str, optional
        """
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        self.session = requests.session()
        self.session.headers = self.headers

        self.img_name = img_name
        self.stream = img_fp

        if isinstance(img_fp, str):
            if img_fp.startswith("http://") or img_fp.startswith("https://"):
                r = self.session.get(img_fp)
                self.stream = BytesIO(r.content)
                self.stream.name = img_fp
            elif os.path.exists(img_fp):
                self.stream = open(img_fp, "rb")
            else:
                raise ValueError("img_fp has no legal meaning as a string!")
        img = Image.open(self.stream)
        self.stream.seek(0)    # 如果不seek到开始位置，之后的上传流读取会产生问题
        if img.format is None: # 这应该不可能发生 :<
            raise ValueError("img_fp does not contain a valid formats!")
        self.img_format = img.format
        if hasattr(self.stream, "name"):
            if img_name is None:
                self.img_name = os.path.splitext(os.path.split(self.stream.name)[1])[0]
        if self.img_name is None:
            self.img_name = "UNKNOWN"

    def __str__(self):
        return f"<ImageUploader img_full_name='{self.img_full_name}' img_format='{self.img_format}'>"

    __repr__=__str__

    def __del__(self):
        if hasattr(self.session, "close"):
            self.session.close()
        if hasattr(self.stream, "close"):
            self.stream.close()

    @property
    def img_full_name(self):
        ext = self.img_format.lower()
        if self.img_format == "JPEG":
            ext = "jpg"
        return f"{self.img_name}.{ext}"

    def upload(self):
        """上传图片文件到smms图床上"""
        fields = {
            "smfile": (self.img_full_name, self.stream, f"image/{self.img_format.lower()}"),
            "file_id": "0"
        }
        m = self._get_multipart_encoder(fields)
        self.headers['Content-Type'] = m.content_type
        r = self.session.post("https://sm.ms/api/upload", data=m, headers=self.headers)
        r.raise_for_status()
        ret_val = r.json()
        if ret_val["code"] == "error":
            self._raise_upload_error(self, ret_val["msg"])
        return upload_result.UploadResult(ret_val["data"])

    def _get_multipart_encoder(self, fields):
        ran_boundary = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        m = MultipartEncoder(fields=fields, boundary=ran_boundary)
        return m

    def _raise_upload_error(self, uploader_obj, msg):
        msg = msg.strip()
        if msg == "No files were uploaded.":
            raise exceptions.UploadNofilesError(uploader_obj, msg)
        elif msg == "File is empty.":
            raise exceptions.UploadEmptyFileError(uploader_obj, msg)
        elif msg == "File is too large.":
            raise exceptions.UploadTooLargeFileError(uploader_obj, msg)
        elif msg == "Upload file count limit.":
            raise exceptions.UploadFileCountLimitError(uploader_obj, msg)
        elif msg == "Upload file frequency limit.":
            raise exceptions.UploadFileCountFrequencyError(uploader_obj, msg)
        elif msg == "Access Denied.":
            raise exceptions.UploadAccessDeniedError(uploader_obj, msg)
        elif msg == "Server error. Upload directory isn't writable.":
            raise exceptions.UploadServerError(uploader_obj, msg)
        raise exceptions.UploadError(uploader_obj, msg)
