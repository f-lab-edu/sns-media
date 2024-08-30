import datetime
import json
import uuid
from typing import Annotated, List, Sequence

from fastapi import Depends, HTTPException
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.apis.posts.schema import CreatePostRequest, GetFollowingPostResponse
from src.cache import redis_client
from src.models.follow import Follow
from src.models.post import Post


class PostService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def get_user_posts(self, user_id: uuid.UUID) -> Sequence[Post]:
        posts = (
            await self.session.exec(select(Post).where(Post.writer == user_id))
        ).all()

        if not posts:
            raise HTTPException(status_code=404, detail="Posts not found")

        return posts

    async def get_user_post(self, user_id: uuid.UUID, post_id: int) -> Post:
        post = await self.session.exec(
            select(Post).where(Post.writer == user_id, Post.id == post_id)
        )
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return post.first()

    async def create_new_post(
        self, request: CreatePostRequest, user_id: uuid.UUID
    ) -> Post:
        post = Post(contents=request.contents, writer=user_id)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)

        return post

    async def get_following_post(self, user_id: uuid.UUID) -> Sequence[Post]:
        posts = await self.session.exec(
            select(Post)
            .select_from(Post)
            .join(Follow, Post.writer == Follow.followee_id)
            .distinct()
            .where(Follow.follower_id == user_id)
            .order_by(col(Post.created_at).desc())
            .limit(100)
        )

        posts = posts.all()

        return posts

    @staticmethod
    def caching_following_posts_list(
        post_data: List[GetFollowingPostResponse], user_id: str
    ):
        cache = redis_client
        data_list = [item.model_dump_json() for item in post_data]
        cache.set(user_id, json.dumps(data_list), datetime.timedelta(seconds=60))

    @staticmethod
    def add_caching_follower_posts_list(post: Post, followers_id: List[uuid.UUID]):
        cache = redis_client

        item = GetFollowingPostResponse(id=post.id)

        for follower_id in followers_id:
            if cache_data := cache.get(str(follower_id)):
                cache_data = json.loads(cache_data)
                cache_data.insert(0, item.model_dump_json())
                if len(cache_data) > 100:
                    cache_data = cache_data[0 : -(len(cache_data) - 100)]
                cache.set(
                    str(follower_id),
                    json.dumps(cache_data),
                    datetime.timedelta(seconds=60),
                )
