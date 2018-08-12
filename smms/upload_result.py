import re
import time

import requests

import smms.exceptions as exceptions


class UploadResult(object):

    _re_del_msg = re.compile(r'<div class="bs-callout bs-callout-warning" style=".*?">(.*?)</div>')

    def __init__(self, data):
        self._data = data  # TODO 对data有效性做检查（我觉得没必要~）

    def __str__(self):
        return f"<SmmsImage img_name='{self.img_name}' smms_url='{self.smms_url}' img_hash='{self.img_hash}'>"

    __repr__=__str__

    @property
    def img_size(self):
        return self._data["width"], self._data["height"]

    @property
    def img_name(self):
        return self._data["filename"]

    @property
    def ip(self):
        return self._data["ip"]

    @property
    def smms_url(self):
        return self._data["url"]

    @property
    def img_hash(self):
        return self._data["hash"]

    @property
    def upload_time(self):
        return time.localtime(self._data["timestamp"])

    @property
    def img_data(self):
        return self._data

    def delete(self):
        r = requests.get(f"https://sm.ms/api/delete/{self.img_hash}")
        r.raise_for_status()
        result = UploadResult._re_del_msg.search(r.text)
        if result is None:
            raise RuntimeError(f"The response string has no legal meaning!")
        msg = result.group(1)
        if msg == "File already deleted.":
            raise exceptions.FileAlreadyDeletedError(self, msg)
        elif msg == "Hash id not found.":
            raise exceptions.HashIdNotFoundError(self, msg)
        elif msg != "File delete success.":
            raise exceptions.FileDeleteError(self, msg)
        
