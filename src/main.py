from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from src import config
from src.apis.common import common_router
from src.apis.follows import follow_router
from src.apis.likes import like_router
from src.apis.posts import post_router
from src.apis.users import user_router
from src.database import close_db, create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(common_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(follow_router)
app.include_router(like_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.origins.split(","),
    allow_credentials=True,
    allow_methods=config.cors.methods.split(","),
    allow_headers=config.cors.headers.split(","),
)

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, include_in_schema=False)


if __name__ == "__main__":
    uvicorn.run(app, host=config.web.host, port=config.web.port)
