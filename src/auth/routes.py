# contains API endpoints that are going to be specific to our users - Authentication
# here we create our Fast API router - A Router Object - Similar to fast APi instance in main.py - from fastapi import APIRouter
from datetime import datetime, timedelta
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import (
    UserCreateModel,
    UserModel,
    UserLoginModel,
    UserWithBookModel,
    EmailModel,
)
from src.db.main import get_session
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken
from src.mail import mail, create_message
from .service import UserService
from .utils import create_access_token, verify_password


from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_logged_in_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the app</h1>"
    subject = "Welcome to our app"

    message = create_message(recipients=emails, subject=subject, body=html)
    await mail.send_message(message)

    return {"message": "Email sent successfully"}

@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exits(email, session)
    if user_exists:
        raise UserAlreadyExists()
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
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
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
        raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    """check if our token is expired & if it's not expired then we create a new access token with the user details that are found withing our tokenF"""

    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})
    # print(expiry_timestamp)

    raise InvalidToken()


@auth_router.get("/me", response_model=UserWithBookModel)
async def get_current_user(
    user: UserModel = Depends(get_current_logged_in_user),
    _: bool = Depends(role_checker),
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    """_summary_
    Our token is added to blocklist and we can no longer use it to access our protected routes

    Args:
        token_details (dict, optional): _description_. Defaults to Depends(AccessTokenBearer()).

    Returns:
        _type_: _description_
    """

    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={"message": "logged out successfully"}, status_code=status.HTTP_200_OK
    )
