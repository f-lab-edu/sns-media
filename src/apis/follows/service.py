import uuid
from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.models.follow import Follow


class FollowService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def create_follow(
        self, followee_id: uuid.UUID, follower_id: uuid.UUID
    ) -> Follow:
        follow: Follow | None = Follow(
            followee_id=followee_id,
            follower_id=follower_id,
            created_at=datetime.utcnow(),
        )

        self.session.add(follow)
        await self.session.commit()
        await self.session.refresh(follow)

        return follow
