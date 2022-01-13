from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": schemas.HTTPError}},
)
async def create_user(
    user_in: schemas.UserCreate, db: AsyncSession = Depends(deps.get_db)
) -> Any:
    user = await crud.user.get_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already exists an user with this email.",
        )
    user = await crud.user.create(db=db, user_in=user_in)
    return user


@router.get(
    "/me",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    responses=deps.GET_TOKEN_USER_RESPONSES
)
async def get_current_user(
    token_user: models.User = Depends(deps.get_token_user),
) -> Any:
    return token_user


@router.put(
    "/me",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES,
)
async def update_current_user(
    user_in: schemas.UserUpdatePUT,
    token_user: models.User = Depends(deps.get_token_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Update your own user.\n
    Note: If the email is updated, the user will be deactivated and the email
     will have to be re-verified. (Unless you are an admin)
    """

    if not token_user.is_superuser:
        # Normal user can't give superuser
        if user_in.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )

        # Deactivate the user
        if user_in.email and user_in.email != token_user.email:
            user_in.is_active = False

    user = await crud.user.update(db=db, db_user=token_user, user_in=user_in)
    return user

@router.delete(
    "/me",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES
)
async def delete_current_user(
    token_user: models.User = Depends(deps.get_token_active_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    await crud.user.delete_by_id(db=db, id=token_user.id)
    return token_user

@router.get(
    "/{user_id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES,
)
async def get_user_by_id(
    user_id: int,
    token_user: models.User = Depends(deps.get_token_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    if token_user.id == user_id:
        return token_user

    if not token_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )

    user = await crud.user.get_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put(
    "/{user_id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    responses=deps.GET_TOKEN_ACTIVE_USER_RESPONSES,
)
async def update_user_by_id(
    user_id: int,
    user_in: schemas.UserUpdatePUT,
    token_user: models.User = Depends(deps.get_token_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Update a user by id.\n
    Note: If the email is updated, the user will be deactivated and the email
     will have to be re-verified. (Unless you are an admin)
    """
    if token_user.id == user_id:

        if not token_user.is_superuser:
            # Normal user can't give superuser
            if user_in.is_superuser:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="The user doesn't have enough privileges",
                )

            # Deactivate the user
            if user_in.email and user_in.email != token_user.email:
                user_in.is_active = False

        updated_user = await crud.user.update(
            db=db, db_user=token_user, user_in=user_in
        )
        return updated_user

    if not token_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )

    db_user = await crud.user.get_by_id(db=db, id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not found"
        )
    updated_user = await crud.user.update(
        db=db, db_user=db_user, user_in=user_in
    )
    return updated_user
