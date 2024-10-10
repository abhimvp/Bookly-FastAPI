from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import (
    HTTPAuthorizationCredentials,
)  # a special class to allow us to get protect an endpoint & make it only access when someone provides their token in the form of Bearer
from .utils import decode_token
from fastapi.exceptions import HTTPException


class AccessTokenBearer(HTTPBearer):
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

        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        # if token_data is not None:
        #     return True
        # else:
        #     return False
        return True if token_data is not None else False
