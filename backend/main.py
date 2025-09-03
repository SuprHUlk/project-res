from fastapi import FastAPI
from backend.api.routes.login import router as loginRouter
from backend.database.mongoDb import set_mongo_client

app = FastAPI()

routers = [
    loginRouter
]

set_mongo_client()

for router in routers:
    app.include_router(router)

