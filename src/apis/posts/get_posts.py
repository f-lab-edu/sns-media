from typing import Annotated

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.apis.posts.get_post import GetPostResponse
from src.apis.users.service import UserService
from src.models.post import Post
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    session: Annotated[AsyncSession, Depends(get_session)],
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
) -> list[GetPostResponse]:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)
    posts = (await session.exec(select(Post).where(Post.writer == user.id))).all()
    return sorted(
        [
            GetPostResponse(
                id=post.id,
                contents=post.contents,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            for post in posts
        ],
        key=lambda post: -post.id,
    )
