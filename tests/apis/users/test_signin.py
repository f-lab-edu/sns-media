import os

import pytest
from fastapi import status
from httpx import AsyncClient
from jose import jwt
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.users.service import UserService
from src.models.user import User


@pytest.mark.asyncio
async def test_signup(client: AsyncClient, session: AsyncSession):
    user_service = UserService(session=session)
    email = "test12@gmail.com"
    password = "<PASSWORD>"

    user: User = User.create(
        email=email,
        password=user_service.hash_password(password=password),
        username="test",
    )
    await user_service.save_user(user=user)

    body = {
        "email": email,
        "password": password,
    }

    response = await client.post("/users/signin", json=body)
    token: str = response.json().get("access_token")
    payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert payload.get("user_id") == str(user.id)
