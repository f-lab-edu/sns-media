import uuid
from typing import Annotated, Sequence

from fastapi import Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.apis.posts.schema import CreatePostRequest
from src.models.post import Post


class PostService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def get_user_posts(self, user_id: uuid.UUID) -> Sequence[Post]:
        posts = (
            await self.session.exec(select(Post).where(Post.writer == user_id))
        ).all()

        if not posts:
            raise HTTPException(status_code=404, detail="Posts not found")

        return posts

    async def get_user_post(self, user_id: uuid.UUID, post_id: int) -> Post:
        post = await self.session.exec(
            select(Post).where(Post.writer == user_id, Post.id == post_id)
        )
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return post.first()

    async def create_new_post(
        self, request: CreatePostRequest, user_id: uuid.UUID
    ) -> Post:
        post = Post(contents=request.contents, writer=user_id)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)

        return post
