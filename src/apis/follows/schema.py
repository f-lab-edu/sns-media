import uuid

from pydantic import BaseModel


class CreateFollowRequest(BaseModel):
    follower_id: uuid.UUID
