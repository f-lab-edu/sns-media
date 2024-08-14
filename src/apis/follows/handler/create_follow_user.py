from fastapi import Depends

from src.apis.follows.schema import CreateFollowRequest
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
) -> Follow:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)

    follow: Follow = await follow_service.create_follow(
        followee_id=user.id, follower_id=follow_request.following_id
    )

    return follow
