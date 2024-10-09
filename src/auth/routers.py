# contains API endpoints that are going to be specific to our users - Authentication
# here we create our Fast API router - A Router Object - Similar to fast APi instance in main.py - from fastapi import APIRouter
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserCreateModel, UserModel
from .service import UserService
from src.db.main import get_session

auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exits(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    else:
        new_user = await user_service.create_user(user_data, session)
        return new_user
