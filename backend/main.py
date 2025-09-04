from fastapi import FastAPI
from backend.api.routes.login import router as loginRouter
from backend.database.mongoDb import set_mongo_client
from backend.models.user import get_user_repo
from contextlib import asynccontextmanager

routers = [
    loginRouter
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await set_mongo_client()
    await get_user_repo().initialize_indexes()
    yield

app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)

