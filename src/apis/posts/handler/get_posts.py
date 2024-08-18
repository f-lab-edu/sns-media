from typing import List

from fastapi import Depends

from src.apis.posts.schema import GetPostResponse
from src.apis.posts.service import PostService
from src.apis.users.service import UserService
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
    post_service: PostService = Depends(),
) -> List[GetPostResponse]:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)
    posts = await post_service.get_user_posts(user_id=user.id)
    return [
        GetPostResponse(
            id=post.id,
            contents=post.contents,
            created_at=post.created_at,
            writer=post.writer,
        )
        for post in posts
    ]
