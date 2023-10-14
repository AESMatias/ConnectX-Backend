from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.models.user import UserFile as DBUserFile
from app.schemas.files import UserFile as SchemaUserFile
from fastapi import APIRouter, HTTPException
import os

files = APIRouter()

@files.post("/uploadimagen/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not os.path.exists("Data"):
        os.makedirs("Data")
    try:
        contents = await file.read()
        with open(os.path.join("Data", file.filename), "wb") as f:
            f.write(contents)
        # Aquí es donde guardamos el archivo en la base de datos
        user_file = SchemaUserFile(user_id=1, file=contents)  # Asegúrate de reemplazar el user_id con el id del usuario correcto
        db_file = DBUserFile(**user_file.dict())
        db.add(db_file)
        db.commit()
    except Exception as e:
        return {"error": str(e)}
    finally:
        await file.close()
    return {"filename": file.filename}
