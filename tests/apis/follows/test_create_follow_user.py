import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.follow import Follow
from src.models.user import User
from tests.apis import create_user_and_get_jwt


@pytest.mark.asyncio
async def test_create_follow_user(client: AsyncClient, session: AsyncSession):
    headers = await create_user_and_get_jwt(session)

    user = User.create(
        email="<EMAIL>",
        password="<PASSWORD>",
        username="test",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    # when
    response = await client.post(
        "/follows",
        json={
            "followee_id": str(user.id),
        },
        headers=headers,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["followee_id"] == str(user.id)

    follow = await session.exec(select(Follow).where(Follow.followee_id == user.id))
    assert follow.first().followee_id == user.id
