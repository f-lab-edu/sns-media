from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.apis.users.schema import UserSignupRequest, UserSignupResponse
from src.apis.users.service import UserService
from src.models.user import User


async def handler(
    request: UserSignupRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    user_service: UserService = Depends(),
):
    hashed_password: str = user_service.hash_password(password=request.password)

    user: User = user_service.save_user(
        session=session,
        user=User.create(
            email=request.email, username=request.username, password=hashed_password
        ),
    )

    return UserSignupResponse.model_validate(user)
