import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.users.service import UserService
from src.models.post import Post
from src.models.user import User


# `GET /posts/{post_id}` API가 성공적으로 동작한다.
@pytest.mark.asyncio
async def test_update_post_successfully(client: AsyncClient, session: AsyncSession):
    user = User(
        email="test@gmail.com",
        password="test1234",
        username="user_name",
    )

    post = Post(contents="test content", writer=user.id)
    session.add_all([post, user])
    await session.commit()
    await session.refresh(post)
    await session.refresh(user)

    user_service = UserService(session)

    jwt = await user_service.create_jwt(user.id)

    headers = {"Authorization": f"Bearer {jwt}"}

    # when
    # `GET /posts/{post_id}` API를 호출한다.
    response = await client.put(
        f"/posts/{post.id}", json={"contents": "test content2"}, headers=headers
    )

    # then
    # 응답 상태 코드가 200이어야 한다.
    assert response.status_code == status.HTTP_200_OK

    # 응답 본문이 예상한 형식과 같아야 한다.
    data = response.json()
    assert data["contents"] == "test content2"
