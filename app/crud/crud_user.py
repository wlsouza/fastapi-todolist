from typing import Optional, Union, List, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class CrudUser():

    def get_by_id(self, db:Session, id:int) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def get_multi(
        self, db:Session, skip:int=0, limit:int=100
    ) -> Optional[List[User]]:
        return db.query(User).offset(skip).limit(limit).all()

    def get_by_email(self, db:Session, email:str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(
        self, db:Session, user_in: Union[UserCreate, Dict[str, Any]]
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
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
        self, db:Session, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
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
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_by_id(self, db:Session, id:int) -> Optional[User]:
        user = self.get_by_id(db=db, id=id)
        db.delete(user)
        db.commit()
        return user

    
user = CrudUser()