from typing import Annotated

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.models.like import Like


class LikeService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def toggle_like(self, user_id: str, post_id: int) -> bool:
        like = await self.session.exec(
            select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
        )

        if like := like.one_or_none():
            await self.session.delete(like)
            await self.session.commit()
            return False

        like = Like(user_id=user_id, post_id=post_id)
        self.session.add(like)
        await self.session.commit()

        return True
