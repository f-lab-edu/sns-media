import datetime
import uuid

from sqlmodel import Field, SQLModel


class Follow(SQLModel, table=True):
    followee_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, primary_key=True
    )
    follower_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, primary_key=True
    )
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
