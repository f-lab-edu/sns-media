from fastapi import APIRouter
from starlette import status

from src.apis.users.handler import sign_in, sign_up

user_router = APIRouter(prefix="/users", tags=["users"])

user_router.add_api_route(
    methods=["POST"],
    path="/signup",
    endpoint=sign_up.handler,
    status_code=status.HTTP_201_CREATED,
)

user_router.add_api_route(
    methods=["POST"],
    path="/signin",
    endpoint=sign_in.handler,
    status_code=status.HTTP_200_OK,
)
