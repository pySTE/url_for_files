from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 1024 * 1024 * 100
ALLOW_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.mp4', '.mp3', '.zip'}
BASE_URL = "http://127.0.0.1:8000"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(413)

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOW_EXT:
        raise HTTPException(400)

    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    try:
        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)
    except Exception as e:
        raise HTTPException(500, detail=str(e))

    file_url = f"{BASE_URL}/files/{unique_name}"
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "filename": unique_name,
            "url": file_url,
            "size": file_size
        }
    )


@router.get("/files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path) or not filename:
        raise HTTPException(404)

    return FileResponse(file_path)
