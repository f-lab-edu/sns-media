import random
import time

import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.follow import Follow
from src.models.post import Post
from src.models.user import User
from tests.apis import create_user_and_get_jwt


@pytest.mark.asyncio
async def test_get_following_posts(client: AsyncClient, session: AsyncSession):
    headers: dict = await create_user_and_get_jwt(session)

    follower_count: int = 100
    posts_count: int = 30

    user_list = [
        User.create(
            email=f"<EMAIL{i}>",
            password=f"<PASSWORD{i}>",
            username=f"test{i}",
        )
        for i in range(follower_count)
    ]

    session.add_all(user_list)
    await session.commit()

    for user in user_list:
        await session.refresh(user)

    user = await session.exec(select(User).where(User.email == "test@gmail.com"))

    user = user.first()

    user_id = str(user.id)

    followers = [
        Follow(follower_id=user.id, followee_id=followee.id) for followee in user_list
    ]

    session.add_all(followers)

    posts = [
        Post(
            contents=f"test{i}",
            writer=user_list[random.randint(0, follower_count - 1)].id,
        )
        for writer in user_list
        for i in range(posts_count)
    ]

    user_ids = [str(user.id) for user in user_list]

    session.add_all(posts)
    await session.commit()

    start_time = time.time()
    response = await client.get(f"/posts/following", headers=headers)
    print(
        "Time took to process the request and return response is {} sec".format(
            time.time() - start_time
        )
    )

    assert response.status_code == 200
    assert len(response.json()) <= 100
    for post in response.json():
        assert post["writer"] in user_ids
        assert post["writer"] != user_id

    start_time = time.time()
    cache_response = await client.get(f"/posts/following", headers=headers)
    print(
        "Time took to process the request and return response is {} sec".format(
            time.time() - start_time
        )
    )

    assert cache_response.status_code == 200
    assert cache_response.json() == response.json()
