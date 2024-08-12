from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.apis.posts.schema import CreatePostRequest, CreatePostResponse
from src.models.post import Post


async def handler(
    request: CreatePostRequest, session: Annotated[AsyncSession, Depends(get_session)]
) -> CreatePostResponse:
    post = Post(
        contents=request.contents,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return CreatePostResponse(
        id=post.id, contents=post.contents, created_at=post.created_at
    )
