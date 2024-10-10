# contains API endpoints that are going to be specific to our users - Authentication
# here we create our Fast API router - A Router Object - Similar to fast APi instance in main.py - from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from .utils import create_access_token, decode_token, verify_password
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2


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


@auth_router.post("/login")
async def login_users(
    user_login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = user_login_data.email
    password = user_login_data.password
    user = await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "message": "Login Successful",
                    "user": {"email": user.email, "uid": str(user.uid)},
                },
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password",
        )
