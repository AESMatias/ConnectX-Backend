from fastapi import APIRouter, UploadFile, File
from typing import List
import os

uploadfiles = APIRouter()

@uploadfiles.post("/uploadimagen/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    if not os.path.exists("Data"):
        os.makedirs("Data")
    for file in files:
        try:
            contents = await file.read()
            with open(os.path.join("Data", file.filename), "wb") as f:
                f.write(contents)
        except Exception as e:
            return {"error": str(e)}
        finally:
            await file.close()
    return {"filenames": [file.filename for file in files]}

