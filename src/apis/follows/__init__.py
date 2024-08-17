from fastapi import APIRouter, status

from src.apis.follows.handler import (
    create_follow_user,
    get_follower_list,
    get_following_list,
)
from src.apis.follows.schema import (
    CreateFollowResponse,
    GetFollowingListResponse,
    GetFollowListResponse,
)

follow_router = APIRouter(prefix="/follows", tags=["follows"])

follow_router.add_api_route(
    methods=["POST"],
    path="",
    endpoint=create_follow_user.handler,
    response_model=CreateFollowResponse,
    status_code=status.HTTP_201_CREATED,
)

follow_router.add_api_route(
    methods=["GET"],
    path="/follower",
    endpoint=get_follower_list.handler,
    response_model=GetFollowListResponse,
    status_code=status.HTTP_200_OK,
)

follow_router.add_api_route(
    methods=["GET"],
    path="/following",
    endpoint=get_following_list.handler,
    response_model=GetFollowingListResponse,
    status_code=status.HTTP_200_OK,
)
