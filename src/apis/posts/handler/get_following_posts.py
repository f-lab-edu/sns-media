import json
from typing import List

from fastapi import Depends, HTTPException

from src.apis.posts.schema import GetPostResponse
from src.apis.posts.service import PostService
from src.apis.users.service import UserService
from src.cache import redis_client
from src.models.user import User
from src.security import get_authorization_header


async def handler(
    access_token: str = Depends(get_authorization_header),
    user_service: UserService = Depends(),
    post_service: PostService = Depends(),
) -> List[GetPostResponse]:
    user_id: str = await user_service.decode_jwt(access_token)
    user: User | None = await user_service.get_user_by_id(user_id)
    cache = redis_client

    if data_list := cache.get(user_id + "post"):
        data_list = json.loads(data_list)
        return [GetPostResponse(**json.loads(item)) for item in data_list]

    post_list = await post_service.get_following_post(user_id=user.id)

    if not post_list:
        raise HTTPException(status_code=404, detail="Post not found")

    data = [
        GetPostResponse(
            id=post.id,
            contents=post.contents,
            writer=post.writer,
            created_at=post.created_at,
        )
        for post in post_list
    ]

    data_list = [item.model_dump_json() for item in data]
    cache.set(user_id + "post", json.dumps(data_list))

    return data
