from typing import Optional, Union, List, Dict, Any
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


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
        pass

    def update(
        self, db:Session, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        pass

    def delete(self, db:Session, db_user:User) -> None:
        pass

    
user = CrudUser()