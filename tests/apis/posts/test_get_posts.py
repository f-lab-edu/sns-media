import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.users.service import UserService
from src.models.post import Post
from src.models.user import User


# `GET /posts` API가 성공적으로 동작한다.
@pytest.mark.asyncio
async def test_get_posts_successfully(client: AsyncClient, session: AsyncSession):
    user = User(
        email="test@gmail.com",
        password="test1234",
        username="user_name",
    )
    # given
    # 서버 내에 여러 개의 Post 데이터가 저장되어 있다.
    post_1 = Post(
        contents="content 1",
    )
    post_2 = Post(
        contents="content 2",
        writer=user.id,
    )
    session.add_all([post_1, post_2, user])
    await session.commit()
    await session.refresh(post_1)
    await session.refresh(post_2)
    await session.refresh(user)

    user_service = UserService(session)

    jwt = await user_service.create_jwt(user.id)

    headers = {"Authorization": f"Bearer {jwt}"}

    # when
    # `GET /posts` API를 호출한다.
    response = await client.get("/posts", headers=headers)

    # then
    # 응답 상태 코드가 200이어야 한다.
    assert response.status_code == status.HTTP_200_OK

    # 응답 본문에는 id가 큰 순서대로 Post 데이터가 포함되어 있어야 한다.
    data = response.json()
    assert data == [
        {
            "id": post_2.id,
            "contents": post_2.contents,
            "created_at": post_2.created_at.isoformat(),
        }
    ]
