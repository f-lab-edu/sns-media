import uuid

from pydantic import BaseModel


class CreateFollowRequest(BaseModel):
    followee_id: uuid.UUID


class CreateFollowResponse(BaseModel):
    followee_id: uuid.UUID
    follower_id: uuid.UUID
