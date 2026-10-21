from enum import Enum
class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "File Type Not Supported"
    FILE_SIZE_EXCEEDED = "File Size Exceeded"
    FILE_VALIDATE_SUCCESS = "File Validated Successfully"
    FILE_UPLOAD_SUCCESS = "File Uploaded Successfully"
    FILE_UPLOAD_FAIL = "File Uploading Failed"