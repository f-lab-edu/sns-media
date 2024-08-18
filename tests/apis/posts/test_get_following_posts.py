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

    user_list = [
        User.create(
            email=f"<EMAIL{i}>",
            password=f"<PASSWORD{i}>",
            username=f"test{i}",
        )
        for i in range(10)
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
        Post(contents=f"{writer.id} test{i}", writer=writer.id)
        for writer in user_list
        for i in range(5)
    ]

    user_ids = [str(user.id) for user in user_list]

    session.add_all(posts)
    await session.commit()

    for follow in followers:
        await session.refresh(follow)

    for post in posts:
        await session.refresh(post)

    response = await client.get(f"/posts/following", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 50
    for post in response.json():
        assert post["writer"] in user_ids
        assert post["writer"] != user_id
