from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.apis.follows.schema import CreateFollowRequest, CreateFollowResponse
from src.apis.follows.service import FollowService
from src.apis.users.service import UserService
from src.models.follow import Follow
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    follow_request: CreateFollowRequest,
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
    follow_service: FollowService = Depends(),
) -> CreateFollowResponse:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)

    try:
        follow: Follow = await follow_service.create_follow(
            followee_id=follow_request.followee_id, follower_id=user.id
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Follow already exists")

    return CreateFollowResponse(
        followee_id=follow.followee_id,
        follower_id=follow.follower_id,
    )
