from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import (
    HTTPAuthorizationCredentials,
)  # a special class to allow us to get protect an endpoint & make it only access when someone provides their token in the form of Bearer
from .utils import decode_token
from fastapi.exceptions import HTTPException


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
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
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
