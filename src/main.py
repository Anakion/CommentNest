import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.v1.routers import comments, ws
from src.core.websocket_manager import manager

# Получаем абсолютный путь к корню проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Переходим на уровень выше (из src в корень проекта)
BASE_DIR = os.path.dirname(PROJECT_ROOT)
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI()

# Подключаем роутеры API
app.include_router(comments.router, prefix="/api/v1")
app.include_router(ws.router, prefix="/api/v1")

# Обслуживание статических файлов
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
