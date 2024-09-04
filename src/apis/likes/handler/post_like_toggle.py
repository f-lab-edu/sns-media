from fastapi import Depends

from src.apis.likes.schema import PostLikeResponse
from src.apis.likes.service import LikeService
from src.apis.users.service import UserService
from src.security import get_authorization_header


async def handler(
    post_id: int,
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
    like_service: LikeService = Depends(),
) -> PostLikeResponse:
    user_id: str = await user_service.decode_jwt(access_token)

    like = await like_service.toggle_like(user_id=user_id, post_id=post_id)

    return PostLikeResponse(status=like)
