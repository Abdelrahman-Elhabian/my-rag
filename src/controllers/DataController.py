from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # Convert MB to bytes

    def _get_file_size(self, file: UploadFile):
        size = getattr(file, "size", None)
        if isinstance(size, (int, float)):
            return int(size)

        headers = getattr(file, "headers", {}) or {}
        content_length = headers.get("content-length") or headers.get("Content-Length")
        if content_length is not None:
            try:
                return int(content_length)
            except (TypeError, ValueError):
                pass

        file_obj = getattr(file, "file", None)
        if file_obj is None:
            return None

        try:
            current_position = file_obj.tell()
            file_obj.seek(0, os.SEEK_END)
            file_size = file_obj.tell()
            file_obj.seek(current_position)
            return file_size
        except (AttributeError, OSError, ValueError):
            return None

    def _is_allowed_content_type(self, file: UploadFile):
        content_type = (getattr(file, "content_type", None) or "").lower()
        allowed_types = {
            str(t).lower().strip() for t in self.app_settings.FILE_ALLOWED_TYPES
        }

        if content_type in allowed_types:
            return True

        filename = (getattr(file, "filename", "") or "").lower()
        if not filename:
            return False

        extension = os.path.splitext(filename)[1]
        generic_types = {"application/octet-stream", "binary/octet-stream", ""}
        if content_type in generic_types:
            extension_map = {
                ".txt": {"text/plain"},
                ".pdf": {"application/pdf"},
                ".py": {"text/plain", "text/x-python", "application/x-python-code"},
            }
            if extension_map.get(extension, set()) & allowed_types:
                return True

            # Some clients omit the MIME type or send a generic octet-stream value
            # even for valid text-based uploads such as .py files.
            if not content_type:
                return extension in {".txt", ".pdf", ".py"}

            return False

        return False

    def file_validation(self, file: UploadFile):
        if not self._is_allowed_content_type(file):
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        file_size = self._get_file_size(file)
        if (
            file_size is not None
            and file_size > self.app_settings.FILE_MAX_SIZE * self.size_scale
        ):
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATE_SUCCESS.value
