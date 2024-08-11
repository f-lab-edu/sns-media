import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)

    @classmethod
    def create(cls, email: str, username: str, password: str) -> "User":
        return cls(email=email, username=username, password=password)

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.email}>"
