import datetime

from sqlmodel import Field, SQLModel


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    contents: str = Field(min_length=1, max_length=500)
    formats: str = Field(min_length=1, max_length=20, default="POST")
    is_deleted: bool = Field(default=False)
    is_hidden: bool = Field(default=False)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
