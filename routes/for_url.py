from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import os
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update
from database.connection import get_db
from encode import int_to_base62
from models.urls import Urls
from config import Config

router = APIRouter()

UPLOAD_DIR = Config.UPLOAD_DIR
MAX_FILE_SIZE = Config.MAX_FILE_SIZE
ALLOW_EXT = Config.ALLOW_EXT
BASE_URL = Config.BASE_URL

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_db)
):
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

    try:
        result = await session.execute(
            insert(Urls).values(
                url=file_url,
                path=unique_name,
                short_path=None
            ).returning(Urls.id))

        url_id = result.scalar_one()
        await session.commit()

        short_path = int_to_base62(url_id)

        await session.execute(
            update(Urls)
            .where(Urls.id == url_id)
            .values(short_path=short_path)
        )
        await session.commit()

        short_url = f"{BASE_URL}/{short_path}"

        return JSONResponse(
            status_code=201,
            content={
                "status": "success",
                "id": url_id,
                "filename": unique_name,
                "url": file_url,
                "short_url": short_url,
                "size": file_size
            }
        )

    except Exception as e:
        await session.rollback()
        raise HTTPException(500, detail=str(e))


@router.get("/files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path) or not filename:
        raise HTTPException(404)

    return FileResponse(file_path)
