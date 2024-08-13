import datetime

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.users.service import UserService
from src.models.post import Post
from src.models.user import User


# 공통적으로 사용되는 사용자 생성 및 JWT 토큰 생성 로직을 함수로 분리
async def create_user_and_get_jwt(session: AsyncSession) -> dict:
    user = User(
        email="test@gmail.com",
        password="test1234",
        username="user_name",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user_service = UserService(session)
    jwt = await user_service.create_jwt(user.id)

    return {"Authorization": f"Bearer {jwt}"}


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
