class UploadError(RuntimeError):
    """上传错误"""

    def __init__(self, uploader_obj, msg):
        self.uploader_obj = uploader_obj
        self.msg = msg

    def __str__(self):
        return f"{self.uploader_obj}：未知上传错误（{self.msg}）"


class UnsupportedFormatError(UploadError):
    """不受支持的格式错误"""

    def __str__(self):
        return f"{self.uploader_obj}：不受支持的格式错误（{self.msg}）"


class UploadAccessDeniedError(UploadError):
    """上传权限受限错误"""

    def __str__(self):
        return f"{self.uploader_obj}：上传权限受限错误（{self.msg}）"


class UploadFileCountLimitError(UploadError):
    """上传文件数量受限错误"""

    def __str__(self):
        return f"{self.uploader_obj}：上传文件数量受限错误（{self.msg}）"


class UploadFileCountFrequencyError(UploadError):
    """上传文件过频错误"""

    def __str__(self):
        return f"{self.uploader_obj}：上传文件过频错误（{self.msg}）"


class UploadNofilesError(UploadError):
    """上传文件失败错误"""

    def __str__(self):
        return f"{self.uploader_obj}：上传文件失败错误（{self.msg}）"


class UploadEmptyFileError(UploadError):
    """上传空文件错误"""

    def __str__(self):
        return f"{self.uploader_obj}：上传空文件错误（{self.msg}）"


class UploadTooLargeFileError(UploadError):
    """上传文件太大错误"""

    def __str__(self):
        return f"{self.uploader_obj}：上传文件太大错误（{self.msg}）"


class UploadServerError(UploadError):
    """上传服务错误"""

    def __str__(self):
        return f"{self.uploader_obj}：上传服务错误（{self.msg}）"


class FileDeleteError(RuntimeError):
    """文件删除错误"""

    def __init__(self, smms_image_obj, msg):
        self.smms_image_obj = smms_image_obj
        self.msg = msg

    def __str__(self):
        return f"{self.smms_image_obj}：未知文件删除错误（{self.msg}）"


class FileAlreadyDeletedError(FileDeleteError):
    """文件已经删除错误"""

    def __str__(self):
        return f"{self.smms_image_obj}：文件已经删除错误（{self.msg}）"


class HashIdNotFoundError(FileDeleteError):
    """hash值未找到错误"""

    def __str__(self):
        return f"{self.smms_image_obj}：hash值未找到错误（{self.msg}）"


class HistoryListError(RuntimeError):
    """历史列表错误"""

    def __init__(self, history_manager_obj, response):
        self.history_manager_obj = history_manager_obj
        self.response = response

    def __str__(self):
        return f"{self.history_manager_obj}：未知历史列表错误：{self.response.text}"


class HistoryListClearError(HistoryListError):
    """历史列表清除错误"""

    def __init__(self, history_manager_obj, response, message=None):
        super().__init__(history_manager_obj, response)
        self.message = message

    def __str__(self):
        return f"{self.history_manager_obj}：历史列表清除错误（{self.message}）：{self.response.text}"


class HistoryListFetchError(HistoryListError):
    """历史列表获取错误"""

    def __str__(self):
        return f"{self.history_manager_obj}：历史列表获取错误：{self.response.text}"
