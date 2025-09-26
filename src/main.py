from fastapi import FastAPI

from src.api.v1.routers.comments import router

app = FastAPI()


app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
