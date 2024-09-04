import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.post import Post
from src.models.user import User
from tests.apis import create_user_and_get_jwt


@pytest.mark.asyncio
async def test_get_post_successfully(client: AsyncClient, session: AsyncSession):
    headers = await create_user_and_get_jwt(session)

    user = User(
        email="<EMAIL1>",
        password="<PASSWORD2>",
        username="user_name",
    )

    post = Post(contents="test content", writer=user.id)
    session.add_all([user, post])
    await session.commit()
    await session.refresh(post)

    post_id = post.id

    # when
    # `GET /posts/{post_id}` API를 호출한다.
    response = await client.post(f"/likes/{post_id}", headers=headers)

    assert response.status_code == 201
    assert response.json()["status"] is True

    response = await client.post(f"/likes/{post_id}", headers=headers)

    assert response.status_code == 201
    assert response.json()["status"] is False
