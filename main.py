import logging

from fastapi import FastAPI, APIRouter
import uvicorn

from app.routers.items import router as items_router
from app.settings import config

logger = logging.getLogger()



test_router = APIRouter()

app = FastAPI()


@test_router.get("/posts")
async def posts():
    return {"posts": "test"}


app.include_router(items_router)
app.include_router(test_router)


@app.get("/")
def read_root():
    return "Server is running."


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.BASE_URL,
        port=config.PORT,
        reload=True,
    )