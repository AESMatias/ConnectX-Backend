from fastapi import UploadFile, File
from typing import List
from pydantic import BaseModel
from schemas.user import User

class FileUploadInfo(BaseModel):
    user: User
    files: List[UploadFile] = File(...)