import pytest
from fastapi import status
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio
async def test_signup(client: AsyncClient, session: AsyncSession):
    response = await client.post("/users/signup")
    assert response.status_code == status.HTTP_201_CREATED
