from fastapi import Depends

from src.apis.users.schema import UserSignupRequest, UserSignupResponse
from src.apis.users.service import UserService
from src.models.user import User


async def handler(
    request: UserSignupRequest,
    user_service: UserService = Depends(),
):
    hashed_password: str = user_service.hash_password(password=request.password)

    user: User = await user_service.save_user(
        user=User.create(
            email=request.email, username=request.username, password=hashed_password
        ),
    )

    return UserSignupResponse.model_validate(user)
