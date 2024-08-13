from fastapi import Depends, HTTPException

from src.apis.users.schema import JWTResponse, UserSigninRequest
from src.apis.users.service import UserService
from src.models.user import User


async def handler(
    request: UserSigninRequest,
    user_service: UserService = Depends(),
):
    user: User | None = await user_service.get_user_by_email(email=request.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    verified: bool = await user_service.verify_password(
        plane_password=request.password, hashed_password=user.password
    )

    if not verified:
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token: str = await user_service.create_jwt(user_id=user.id)

    return JWTResponse(access_token=access_token)
