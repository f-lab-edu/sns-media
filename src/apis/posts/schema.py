import datetime

from pydantic import BaseModel, Field


class CreatePostRequest(BaseModel):
    contents: str = Field(max_length=500)


class CreatePostResponse(BaseModel):
    id: int
    contents: str
    created_at: datetime.datetime


class GetPostResponse(BaseModel):
    id: int
    contents: str
    created_at: datetime.datetime
