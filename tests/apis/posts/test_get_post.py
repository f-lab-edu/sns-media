import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.users.service import UserService
from src.models.post import Post
from src.models.user import User


# `GET /posts/{post_id}` API가 성공적으로 동작한다.
@pytest.mark.asyncio
async def test_get_post_successfully(client: AsyncClient, session: AsyncSession):
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
    response = await client.get(f"/posts/{post.id}", headers=headers)

    # then
    # 응답 상태 코드가 200이어야 한다.
    assert response.status_code == status.HTTP_200_OK

    # 응답 본문이 예상한 형식과 같아야 한다.
    data = response.json()
    assert data == {
        "id": post.id,
        "contents": post.contents,
        "writer": str(post.writer),
        "created_at": post.created_at.isoformat(),
    }


# `GET /posts/{post_id}` API가 존재하지 않는 Post ID에 대해서는 404를 응답한다.
@pytest.mark.asyncio
async def test_get_post_with_non_existing_post_id(
    client: AsyncClient, session: AsyncSession
):
    user = User(
        email="test@gmail.com",
        password="test1234",
        username="user_name",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    post_id = 0

    user_service = UserService(session)

    jwt = await user_service.create_jwt(user.id)

    headers = {"Authorization": f"Bearer {jwt}"}

    # when
    # `GET /posts/{post_id}` API를 호출한다.
    response = await client.get(f"/posts/{post_id}", headers=headers)

    # then
    # 응답 상태 코드가 404이어야 한다.
    assert response.status_code == status.HTTP_404_NOT_FOUND
