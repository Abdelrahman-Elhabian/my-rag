from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
import os
from controllers import DataController, ProjectController
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload(
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings),
):
    data_controller = DataController()
    # Browsers and API clients may send a path along with the filename.
    # Store only the filename so the upload cannot escape the project folder.
    filename = os.path.basename((file.filename or "").replace("\\", "/"))
    if not filename:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": "A filename is required"},
        )

    # Validate the file properties
    is_valid, result_signal = data_controller.file_validation(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"signal": result_signal}
        )
    # else:
    #     return {"signal": result_signal}

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = data_controller.generate_unique_filename(orig_filename=file.filename, project_id=project_id)

    total_size = 0
    size_limit = app_settings.FILE_MAX_SIZE * 1048576
    try:
        await file.seek(0)
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                total_size += len(chunk)
                if total_size > size_limit:
                    break
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAIL.value},
        )

    if total_size > size_limit:
        if os.path.exists(file_path):
            os.remove(file_path)
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={"signal": ResponseSignal.FILE_SIZE_EXCEEDED.value},
        )

    return JSONResponse(content={"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value})
