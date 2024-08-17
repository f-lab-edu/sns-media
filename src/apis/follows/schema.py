import uuid
from typing import List

from pydantic import BaseModel


class CreateFollowRequest(BaseModel):
    followee_id: uuid.UUID


class CreateFollowResponse(BaseModel):
    followee_id: uuid.UUID
    follower_id: uuid.UUID


class GetFollowListResponse(BaseModel):
    follower_list: List[uuid.UUID]


class GetFollowingListResponse(BaseModel):
    following_list: List[uuid.UUID]
