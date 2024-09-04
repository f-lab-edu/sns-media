from fastapi import Depends, HTTPException, status

from src.apis.posts.schema import GetPostResponse
from src.apis.posts.service import PostService
from src.apis.users.service import UserService
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    post_id: int,
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
    post_service: PostService = Depends(),
) -> GetPostResponse:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)
    post = await post_service.get_user_post(post_id=post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GetPostResponse(
        id=post.id,
        contents=post.contents,
        writer=post.writer,
        created_at=post.created_at,
    )
