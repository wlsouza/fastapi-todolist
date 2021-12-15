from typing import Optional, Union, List, Dict, Any, Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class CrudUser():

    async def get_by_id(self, db:AsyncSession, id:int) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.id == id)
        )
        return result.scalar()

    async def get_multi(
        self, db:AsyncSession, skip:int=0, limit:int=100
    ) -> Optional[List[User]]:
        result = await db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
        
    async def get_by_email(self, db:AsyncSession, email:str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar()

    async def create(
        self, db:AsyncSession, user_in: Union[UserCreate, Dict[str, Any]]
    ) -> User:
        if isinstance(user_in, dict):
            user_data = user_in.copy()
        else:
            user_data = user_in.dict(exclude_unset=True)
        if user_data.get("password"):
            hashed_password = get_password_hash(user_data.pop("password"))
            user_data["hashed_password"] = hashed_password
        db_user = User(**user_data)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def update(
        self, db:AsyncSession, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(user_in, dict):
            update_data = user_in.copy()
        else:
            update_data = user_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data.pop("password"))
            update_data["hashed_password"] = hashed_password
        for field, value in update_data.items():
            if hasattr(db_user, field):
                setattr(db_user, field, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def delete_by_id(self, db:AsyncSession, id:int) -> Optional[User]:
        user = await self.get_by_id(db=db, id=id)
        await db.delete(user)
        await db.commit()
        return user

    # TODO: Think if authenticate_user method should be in CrudUser class 
    async def authenticate_user(self, db:AsyncSession, user_email:str , password:str) -> Union[Literal[False],User]:
        user = await self.get_by_email(db, user_email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    
user = CrudUser()