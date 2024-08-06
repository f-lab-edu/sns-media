from typing import Annotated

import bcrypt
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.user import User


class UserService:
    encoding = "UTF-8"

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            password.encode(self.encoding),
            bcrypt.gensalt(),
        )
        return hashed_password.decode(self.encoding)

    def save_user(
        self, user: User, session: Annotated[AsyncSession, Depends()]
    ) -> User:
        session.add(user)
        session.commit()
        session.refresh(user)

        return user
