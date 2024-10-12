from typing import Any, List
from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import (
    HTTPAuthorizationCredentials,
)  # a special class to allow us to get protect an endpoint & make it only access when someone provides their token in the form of Bearer
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from .utils import decode_token
from .service import UserService
from .models import User

user_service = UserService()


# created a dependency that will be injected into every path handler that will require an access token to allow us access to resources
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        # check if provided token is actual access token
        # print(creds.scheme) #Bearer
        # print(creds.credentials) #gives us access token
        token = creds.credentials
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token",
                },
            )

        # once we check if our token is vali above then we need to check if the token is in our blocklisrt

        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token",
                },
            )

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        # if token_data is not None:
        #     return True
        # else:
        #     return False
        return True if token_data is not None else False

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(TokenBearer):
    """
    check if valid access token is provided to an endpoint

    Args:
        TokenBearer (_type_): _description_
    """

    def verify_token_data(self, token_data: dict) -> None:
        """check if a refresh token is sent to token that requires an access token &
        then it's going to throw an error if we provide refresh token instead of access token
        """
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):
    """
    check if valid refresh token is provided to an endpoint

    Args:
        TokenBearer (_type_): _description_
    """

    def verify_token_data(self, token_data: dict) -> None:
        """check if a refresh token is sent to token that requires an access token & then it's going to throw an error if we provide refresh token instead of access token"""
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an refresh token",
            )


async def get_current_logged_in_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    """
    In Fast APi , we can create dependencies which will also take in other dependencies : for example
    if we want to get a currently logged in user within our application , we create this function
    This function will take in the token details provided via the Authorization header and extract the user from AccessBearerToken Dependency and return the current user
    """
    print(token_details)
    user_email = token_details["user"]["email"]
    # above we got the email and we need session dependency
    user = await user_service.get_user_by_email(user_email, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    # define the main class that's going to be called each time we create objects
    # for this specific class : RoleChecker , that we inject in those specific path handlers

    def __call__(self, current_user: User = Depends(get_current_logged_in_user)) -> Any:
        """this will check if we're providing a role when accesssing a specific endpoint
        Here we remove *args: Any, **kwds: Any and provide a dependency and this dependency will
        be our get_current_logged_in_user dependency"""
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )
