import uuid

import bcrypt
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(nullable=False)
    hashed_password: str

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = str(bcrypt.hashpw(password.encode("utf-8"), salt))
        self.hashed_password = hashed_password
