from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.for_url import router

UPLOAD_DIR = "uploads"

app = FastAPI()

app.include_router(router)


app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")
