from typing import Sequence

from fastapi import Depends

from src.apis.users.schema import UserResponse
from src.apis.users.service import UserService
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    user_service: UserService = Depends(),
    access_token: str = Depends(get_authorization_header),
):
    await user_service.decode_jwt(access_token)
    user_list: Sequence[User] = await user_service.get_users_list()
    return [
        UserResponse(
            id=user.id,
        )
        for user in user_list
    ]
