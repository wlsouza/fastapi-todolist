
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.user import fake, random_user_dict

# TODO: create a function in utils to insert a random user on db and return it.
# Are only 2 lines, is it worth it? ... 🤔

@pytest.mark.asyncio
async def test_create_user_by_schema(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    user_in = UserCreate(**user_dict) 
    new_user = await crud.user.create(db=db, user_in=user_in)
    assert new_user.email == user_in.email

@pytest.mark.asyncio
async def test_create_user_by_dict(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    assert new_user.email == user_dict["email"]

@pytest.mark.asyncio
async def test_when_create_user_return_hashed_password(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    user_in = UserCreate(**user_dict) 
    new_user = await crud.user.create(db=db, user_in=user_in)
    assert hasattr(new_user, "hashed_password")

@pytest.mark.asyncio
async def test_when_create_user_if_attribute_is_active_is_not_set_it_must_be_false(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    assert new_user.is_active == False

@pytest.mark.asyncio
async def test_when_create_user_if_attribute_is_superuser_is_not_set_it_must_be_false(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    assert new_user.is_superuser == False

@pytest.mark.asyncio
async def test_if_get_by_email_return_correct_user(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    returned_user = await crud.user.get_by_email(db=db, email=user_dict["email"])
    assert returned_user.email == user_dict["email"]

@pytest.mark.asyncio
async def test_if_get_by_id_return_correct_user(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    returned_user = await crud.user.get_by_id(db=db, id=new_user.id)
    assert new_user.email == returned_user.email

@pytest.mark.asyncio
async def test_if_delete_by_id_really_delete_the_user(db: AsyncSession):
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    await crud.user.delete_by_id(db=db, id=new_user.id)
    returned_user = await crud.user.get_by_id(db=db, id=new_user.id)
    assert returned_user == None

@pytest.mark.asyncio
async def test_update_user_by_userupdate_schema(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    new_user = await crud.user.create(db=db, user_in=user_dict)
    user_update_in = UserUpdate(email=fake.free_email())
    updated_user = await crud.user.update(db=db, db_user=new_user, user_in=user_update_in)
    assert updated_user.email == user_update_in.email

@pytest.mark.asyncio
async def test_update_user_by_dict(db: AsyncSession) -> None:
   user_dict = random_user_dict()
   new_user = await crud.user.create(db=db, user_in=user_dict)
   user_update_in = {"email": fake.free_email()}
   updated_user = await crud.user.update(db=db, db_user=new_user, user_in=user_update_in)
   assert updated_user.email == user_update_in["email"]

@pytest.mark.asyncio
async def test_if_get_multi_return_a_list_of_users(db: AsyncSession) -> None:
    user_dict = random_user_dict()
    await crud.user.create(db=db, user_in=user_dict)
    users = await crud.user.get_multi(db=db, limit=1)
    assert isinstance(users, list)


@pytest.mark.asyncio
async def test_if_get_multi_return_the_correct_quantity_of_user(db: AsyncSession) -> None:
    for _ in range(3):
        user_dict = random_user_dict()
        await crud.user.create(db=db, user_in=user_dict)
    users = await crud.user.get_multi(db=db, limit=2)
    assert len(users) == 2

@pytest.mark.asyncio
async def test_if_get_multi_skip_the_correct_quantity_of_user(db: AsyncSession) -> None:
    for _ in range(3):
        user_dict = random_user_dict()
        await crud.user.create(db=db, user_in=user_dict)
    users = await crud.user.get_multi(db=db, skip=2,  limit=1)
    assert users[0].id == 3