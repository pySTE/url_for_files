import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import APIKeyHeader
from sqlalchemy import insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt


from config import Config
from database.connection import get_db
from encode import int_to_base62
from models.urls import Urls
from utils.jwt_handler import verify_access_token

router = APIRouter()

UPLOAD_DIR = Config.UPLOAD_DIR
MAX_FILE_SIZE = Config.MAX_FILE_SIZE
ALLOW_EXT = Config.ALLOW_EXT
BASE_URL = Config.BASE_URL

os.makedirs(UPLOAD_DIR, exist_ok=True)

api_key_header = APIKeyHeader(name="Authorization", auto_error=True)


@router.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        token: str = Depends(api_key_header),
        session: AsyncSession = Depends(get_db)
):
    email = verify_access_token(token)
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
                short_path=None,
                user_email=email

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
        raise HTTPException(500)


@router.get("/files/{filename}")
async def get_file(
        filename: str,
        token: str = Depends(api_key_header),
        session: AsyncSession = Depends(get_db)
):
    email = verify_access_token(token)

    result = await session.execute(
        select(Urls).where(Urls.path == filename)
    )
    file_record = result.scalar_one_or_none()

    if not file_record or file_record.user_email != email:
        raise HTTPException(404)

    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(404)

    return FileResponse(file_path)