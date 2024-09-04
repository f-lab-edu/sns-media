import uuid

from sqlmodel import Field, SQLModel


class Like(SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=True, primary_key=True)
    post_id: int = Field(foreign_key="post.id", nullable=True, primary_key=True)

    def __repr__(self) -> str:
        return f"Like(user_id={self.user_id}, post_id={self.post_id})"
