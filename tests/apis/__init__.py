from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.users.service import UserService
from src.models.user import User


async def create_user_and_get_jwt(session: AsyncSession) -> dict:
    user = User(
        email="test@gmail.com",
        password="<PASSWORD>",
        username="user_name",
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user_service = UserService(session)
    jwt = await user_service.create_jwt(user.id)

    return {"Authorization": f"Bearer {jwt}"}
