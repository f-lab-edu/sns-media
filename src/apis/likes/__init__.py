from fastapi import APIRouter, status

from src.apis.likes.handler import post_like_toggle
from src.apis.likes.schema import PostLikeResponse

like_router = APIRouter(prefix="/likes", tags=["posts"])

like_router.add_api_route(
    methods=["POST"],
    path="/{post_id}",
    endpoint=post_like_toggle.handler,
    status_code=status.HTTP_201_CREATED,
    response_model=PostLikeResponse,
)
