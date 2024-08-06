import uuid

from pydantic import BaseModel


class UserSignupRequest(BaseModel):
    email: str
    password: str
    username: str


class UserSignupResponse(BaseModel):
    id: uuid.UUID
    email: str
    username: str

    class Config:
        from_attributes = True
