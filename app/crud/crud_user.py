from typing import Optional, Union, List, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class CrudUser():

    def get_by_id(self, db:Session) -> Optional[User]:
        pass

    def get_multi_by_id(
        self, db:Session, skip:int=0, limit:int=100
    ) -> Optional[List[User]]:
        pass

    def get_by_email(self, db:Session, email:str) -> Optional[User]:
        pass

    def create(
        self, db:Session, user_in: Union[UserCreate, Dict[str, Any]]
    ) -> User:
        if isinstance(user_in, dict):
            user_data = user_in
        else:
            user_data = user_in.dict(exclude_unset=True)
        db_user = User(
            full_name= user_data["full_name"], 
            email= user_data["email"],
            hashed_password= get_password_hash(user_data["password"])
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(
        self, db:Session, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        pass

    def delete(self, db:Session, db_user:User) -> None:
        pass

    
user = CrudUser()