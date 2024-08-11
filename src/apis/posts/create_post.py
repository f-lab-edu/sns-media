import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.models.post import Post


class CreatePostRequest(BaseModel):
    contents: str = Field(max_length=500)


class CreatePostResponse(BaseModel):
    id: int
    contents: str
    created_at: datetime.datetime


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
