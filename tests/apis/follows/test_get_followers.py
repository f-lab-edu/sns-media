import asyncio

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.follow import Follow
from src.models.user import User
from tests.apis import create_user_and_get_jwt


@pytest.mark.asyncio
async def test_get_followers(client: AsyncClient, session: AsyncSession):
    headers: dict = await create_user_and_get_jwt(session)

    user_list = [
        User.create(
            email=f"<EMAIL{i}>",
            password=f"<PASSWORD{i}>",
            username=f"test{i}",
        )
        for i in range(10)
    ]

    session.add_all(user_list)
    await session.commit()

    refresh_task = set()
    for user in user_list:
        task = asyncio.create_task(session.refresh(user))
        refresh_task.add(task)
    await asyncio.gather(*refresh_task)

    user = await session.exec(select(User).where(User.email == "test@gmail.com"))

    user = user.first()

    followers = [
        Follow(follower_id=follower.id, followee_id=user.id) for follower in user_list
    ]

    session.add_all(followers)
    await session.commit()

    for follow in followers:
        await session.refresh(follow)

    response = await client.get(
        "/follows/follower",
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["follower_list"]) == 10
    for follow in followers:
        assert str(follow.follower_id) in response.json()["follower_list"]


@pytest.mark.asyncio
async def test_get_followers_not_follow(client: AsyncClient, session: AsyncSession):
    headers: dict = await create_user_and_get_jwt(session)

    response = await client.get(
        "/follows/follower",
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "follower not found"}
