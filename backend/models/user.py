from typing import Optional
from pydantic import BaseModel
from pydantic_mongo import AsyncAbstractRepository, PydanticObjectId
from backend.database.mongoDb import get_mongo_client

class User(BaseModel):
    id: Optional[PydanticObjectId] = None
    email: Optional[str] = "testUser" 
    password: Optional[str] = "resumeplusplus"
    is_guest_user: Optional[bool] = False


class UserRepository(AsyncAbstractRepository[User]):
    class Meta:
        collection_name = 'users'

def get_user_repo():
    mongo_client = get_mongo_client()
    return UserRepository(mongo_client)

async def save_user(user: User):
    try:
       await get_user_repo().save(user)
    except Exception as exc:
        raise exc

# async def get_user_id(id)


# Example usage
# user = User(name='John Doe', email='john@example.com')
# await user_repo.save(user)

# user = await user_repo.find_one_by_id(user_id)