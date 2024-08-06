from fastapi import APIRouter
from starlette import status

from src.apis.users import sign_up

user_router = APIRouter(prefix="/users", tags=["users"])

user_router.add_api_route(
    methods=["POST"],
    path="/signup",
    endpoint=sign_up.handler,
    status_code=status.HTTP_201_CREATED,
)
