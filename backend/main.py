from fastapi import FastAPI
from backend.api.routes.login import router as loginRouter
from backend.database.mongoDb import set_mongo_client
from backend.models.user import get_user_repo
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

routers = [
    loginRouter
]

origins = [
    "http://localhost:3000"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await set_mongo_client()
    await get_user_repo().initialize_indexes()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)

