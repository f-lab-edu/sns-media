from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


def get_authorization_header(
    auth_header: HTTPAuthorizationCredentials
    | None = Depends(HTTPBearer(auto_error=False)),
) -> str:
    if auth_header is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    return auth_header.credentials
