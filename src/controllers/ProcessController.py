from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super.__init__
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

        def get_file_extinsion(self, file_id: str):
            return os.path.splitext(file_id)[-1] # Get file extinsion

    