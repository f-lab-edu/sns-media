import json
from typing import List

from fastapi import BackgroundTasks, Depends, HTTPException

from src.apis.posts.schema import GetFollowingPostResponse
from src.apis.posts.service import PostService
from src.apis.users.service import UserService
from src.cache import redis_client
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    background_tasks: BackgroundTasks,
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
    post_service: PostService = Depends(),
) -> List[GetFollowingPostResponse]:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)
    cache = redis_client

    if data_list := cache.get(user_id):
        data_list = json.loads(data_list)
        return [GetFollowingPostResponse(**json.loads(item)) for item in data_list]

    post_list = await post_service.get_following_post(user_id=user.id)

    if not post_list:
        raise HTTPException(status_code=404, detail="Post not found")

    data = [GetFollowingPostResponse(id=post.id) for post in post_list]

    if not cache.get(user_id):
        background_tasks.add_task(
            post_service.caching_following_posts_list,
            post_data=data,
            user_id=user_id,
        )

    return data
