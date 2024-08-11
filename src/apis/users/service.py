import os
import uuid
from datetime import datetime, timedelta
from typing import Annotated, Type

import bcrypt
from fastapi import Depends
from jose import jwt
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.models.user import User


class UserService:
    encoding = "UTF-8"
    secret_key = os.environ.get("SECRET_KEY")
    jwt_algorithm = "HS256"

    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            password.encode(self.encoding),
            bcrypt.gensalt(),
        )
        return hashed_password.decode(self.encoding)

    async def save_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_user_by_email(self, email: str) -> Type[User] | None:
        user = await self.session.scalar(select(User).where(User.email == email))
        return user

    async def get_user_by_id(self, user_id: str) -> Type[User] | None:
        user = await self.session.scalar(select(User).where(User.id == user_id))
        return user

    async def verify_password(self, plane_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plane_password.encode(self.encoding),
            hashed_password.encode(self.encoding),
        )

    async def create_jwt(self, user_id: uuid.UUID) -> str:
        return jwt.encode(
            {
                "user_id": str(user_id),
                "exp": datetime.now() + timedelta(hours=3),
            },
            self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    async def decode_jwt(self, access_token: str) -> str:
        payload: dict = jwt.decode(
            access_token,
            self.secret_key,
            algorithms=self.jwt_algorithm,
        )
        return payload["user_id"]
