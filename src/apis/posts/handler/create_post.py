import uuid
from typing import List

from fastapi import Depends

from src.apis.follows.service import FollowService
from src.apis.posts.schema import CreatePostRequest, CreatePostResponse
from src.apis.posts.service import PostService
from src.apis.users.service import UserService
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    request: CreatePostRequest,
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
    follow_service: FollowService = Depends(),
    post_service: PostService = Depends(),
) -> CreatePostResponse:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)
    post = await post_service.create_new_post(request=request, user_id=user.id)
    followers_id: List[uuid.UUID] = await follow_service.get_follower_list(
        uuid.UUID(user_id)
    )
    post_service.add_caching_follower_posts_list(post, followers_id)

    return CreatePostResponse(
        id=post.id, contents=post.contents, created_at=post.created_at
    )
