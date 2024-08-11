import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_signup(client: AsyncClient, session: AsyncSession):
    body = {
        "email": "test12@gmail.com",
        "password": "1q2w3e4r!",
        "username": "testuser",
    }

    response = await client.post("/users/signup", json=body)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == body["email"]
    assert response.json()["username"] == body["username"]
