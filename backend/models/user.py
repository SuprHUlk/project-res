from typing import Optional, Union
from pydantic import BaseModel, Field
from pydantic_mongo import AsyncAbstractRepository, PydanticObjectId
from backend.database.mongoDb import get_mongo_client

class User(BaseModel):
    id: Optional[PydanticObjectId] = None
    email: Optional[str] = "testUser" 
    password: Optional[str] = "resumeplusplus"
    is_guest_user: Optional[bool] = Field(default=False, alias="isGuestUser")
    
    class Config:
        populate_by_name = True


class UserRepository(AsyncAbstractRepository[User]):
    class Meta:
        collection_name = 'users'

    async def initialize_indexes(self):
        collection = self.get_collection()
        await collection.create_index('email', unique=True)

async def save_user(user: User):
    try:
        await get_user_repo().save(user)    
    except Exception as exc:
        raise exc
    
async def exists(user: User) -> Union[User, None]:
    try:
        user = await get_user_repo().find_one_by({"email": user.email})
        return user if user else None
    except Exception as exc:
        raise exc

def get_user_repo():
    mongo_client = get_mongo_client()
    repo = UserRepository(mongo_client)
    return repo