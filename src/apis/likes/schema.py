from pydantic import BaseModel


class PostLikeResponse(BaseModel):
    status: bool
