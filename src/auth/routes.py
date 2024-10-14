# contains API endpoints that are going to be specific to our users - Authentication
# here we create our Fast API router - A Router Object - Similar to fast APi instance in main.py - from fastapi import APIRouter
from datetime import datetime, timedelta
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken , UserNotFound
from src.mail import mail, create_message
from src.config import Config
from .schemas import (
    UserCreateModel,
    UserModel,
    UserLoginModel,
    UserWithBookModel,
    EmailModel,
)
from .service import UserService
from .utils import (
    create_access_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
)


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
    "/signup", status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exits(email, session)
    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[email], subject="Verify your email", body=html_message
    )

    await mail.send_message(message)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user,
    }

@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user({'is_verified':True},user,session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

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
