import pytest
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User
from tests.apis import create_user_and_get_jwt


@pytest.mark.asyncio
async def test_get_user_list(client: AsyncClient, session: AsyncSession):
    headers = await create_user_and_get_jwt(session)

    user = User.create(
        email="<EMAIL>",
        username="test",
        password="<PASSWORD>",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    response = await client.get(
        "/users/list",
        headers=headers,
    )

    assert response.status_code == 200
