from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from models.urls import Urls
from config import Config

router_shortener = APIRouter()

UPLOAD_DIR = Config.UPLOAD_DIR


@router_shortener.get("/{short_path}")
async def redirect_short_url(short_path: str, session: AsyncSession = Depends(get_db)):
    stmt = select(Urls.url).where(Urls.short_path == short_path)
    result = await session.execute(stmt)
    url_record = result.scalar_one_or_none()

    if not url_record:
        raise HTTPException(404)

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=url_record)
