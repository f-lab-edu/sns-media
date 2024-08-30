import datetime

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.users.service import UserService
from src.models.follow import Follow
from src.models.post import Post
from src.models.user import User
from tests.apis import create_user_and_get_jwt


@pytest.mark.asyncio
async def test_create_post_successfully(client: AsyncClient, session: AsyncSession):
    headers = await create_user_and_get_jwt(session)

    # when
    response = await client.post(
        "/posts",
        json={
            "contents": "content",
        },
        headers=headers,
    )

    # then
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data == {
        "id": 1,
        "contents": "content",
        "created_at": data["created_at"],
    }

    post = await session.get(Post, 1)
    assert post.id == 1
    assert post.contents == "content"
    assert post.created_at == datetime.datetime.fromisoformat(data["created_at"])


@pytest.mark.asyncio
async def test_create_post_failed_by_title_validation(
    client: AsyncClient, session: AsyncSession
):
    headers = await create_user_and_get_jwt(session)

    # when
    response = await client.post(
        "/posts",
        json={
            "content": "content",
        },
        headers=headers,
    )

    # then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_post_failed_by_content_validation(
    client: AsyncClient, session: AsyncSession
):
    headers = await create_user_and_get_jwt(session)

    # given
    contents = "a" * 501

    # when
    response = await client.post(
        "/posts",
        json={
            "title": "title",
            "contents": contents,
        },
        headers=headers,
    )

    # then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_post_follower_posts_update(
    client: AsyncClient, session: AsyncSession
):
    headers = await create_user_and_get_jwt(session)

    user = (
        await session.exec(select(User).where(User.email == "test@gmail.com"))
    ).first()
    user_id = user.id

    follow_user = User.create(
        email="<EMAIL>12",
        password="<PASSWORD>",
        username="test",
    )

    session.add(follow_user)
    await session.commit()
    await session.refresh(follow_user)

    follower_user_id = follow_user.id

    follow = Follow(
        followee_id=user_id,
        follower_id=follower_user_id,
    )

    session.add(follow)
    await session.commit()

    for i in range(10):
        session.add(Post(contents=f"contents{i}", writer=user_id))
    await session.commit()

    user_service = UserService(session)
    jwt = await user_service.create_jwt(follower_user_id)

    follow_user_headers = {"Authorization": f"Bearer {jwt}"}

    follow_user_response = await client.get(
        f"/posts/following", headers=follow_user_headers
    )

    assert follow_user_response.status_code == status.HTTP_200_OK

    response = await client.post(
        "/posts",
        json={
            "contents": "fan out content",
        },
        headers=headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    follow_user_response = await client.get(
        f"/posts/following", headers=follow_user_headers
    )

    assert follow_user_response.status_code == status.HTTP_200_OK
    assert len(follow_user_response.json()) == 11
