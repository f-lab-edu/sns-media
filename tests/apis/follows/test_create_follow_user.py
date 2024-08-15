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


@pytest.mark.asyncio
async def test_create_follow_user_already_exists(
    client: AsyncClient, session: AsyncSession
):
    headers = await create_user_and_get_jwt(session)
    user = User.create(
        email="<EMAIL>",
        password="<PASSWORD>",
        username="test",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    await client.post(
        "/follows",
        json={
            "followee_id": str(user.id),
        },
        headers=headers,
    )

    response = await client.post(
        "/follows",
        json={
            "followee_id": str(user.id),
        },
        headers=headers,
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def two_follow_users(client: AsyncClient, session: AsyncSession):
    headers = await create_user_and_get_jwt(session)
    user1 = User.create(
        email="<EMAIL1>",
        password="<PASSWORD>",
        username="test",
    )
    user2 = User.create(
        email="<EMAIL2>",
        password="<PASSWORD>",
        username="test",
    )

    session.add_all([user1, user2])
    await session.commit()
    await session.refresh(user1)
    await session.refresh(user2)

    response1 = await client.post(
        "/follows",
        json={
            "followee_id": str(user1.id),
        },
        headers=headers,
    )

    assert response1.status_code == status.HTTP_201_CREATED

    response2 = await client.post(
        "/follows",
        json={
            "followee_id": str(user2.id),
        },
        headers=headers,
    )

    assert response2.status_code == status.HTTP_201_CREATED
