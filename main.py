from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.for_url import router
from routes.shortener import router_shortener
from routes.authentication import auth_router

UPLOAD_DIR = "uploads"

app = FastAPI()

app.include_router(router)
app.include_router(router_shortener)
app.include_router(auth_router)


app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")
