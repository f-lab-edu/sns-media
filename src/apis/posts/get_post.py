from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.apis.posts.schema import GetPostResponse
from src.models.post import Post


async def handler(
    post_id: int, session: Annotated[AsyncSession, Depends(get_session)]
) -> GetPostResponse:
    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return GetPostResponse(
        id=post.id,
        contents=post.contents,
        created_at=post.created_at,
    )
