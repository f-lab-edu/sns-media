import uuid
from typing import List

from fastapi import Depends, HTTPException

from src.apis.follows.schema import GetFollowListResponse
from src.apis.follows.service import FollowService
from src.apis.users.service import UserService
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
    follow_service: FollowService = Depends(),
) -> GetFollowListResponse:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)

    follower_list: List[uuid.UUID] = await follow_service.get_follower_list(
        user_id=user.id
    )

    print(follower_list)

    if not follower_list:
        raise HTTPException(status_code=404, detail="follower not found")

    return GetFollowListResponse(follower_list=follower_list)
