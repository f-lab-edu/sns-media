from fastapi import APIRouter, status

from src.apis.follows.handler import create_follow_user
from src.apis.follows.schema import CreateFollowRequest

follow_router = APIRouter(prefix="/follows", tags=["follows"])

follow_router.add_api_route(
    methods=["POST"],
    path="",
    endpoint=create_follow_user.handler,
    response_model=CreateFollowRequest,
    status_code=status.HTTP_201_CREATED,
)
