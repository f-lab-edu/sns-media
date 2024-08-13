from fastapi import APIRouter, status

from src.apis.posts.handler import create_post, get_post, get_posts
from src.apis.posts.schema import CreatePostResponse, GetPostResponse

post_router = APIRouter(prefix="/posts", tags=["posts"])

post_router.add_api_route(
    methods=["POST"],
    path="",
    endpoint=create_post.handler,
    response_model=schema.CreatePostResponse,
    status_code=status.HTTP_201_CREATED,
)
post_router.add_api_route(
    methods=["GET"],
    path="",
    endpoint=get_posts.handler,
    response_model=list[GetPostResponse],
    status_code=status.HTTP_200_OK,
)

post_router.add_api_route(
    methods=["GET"],
    path="/{post_id}",
    endpoint=get_post.handler,
    response_model=GetPostResponse,
    status_code=status.HTTP_200_OK,
)
