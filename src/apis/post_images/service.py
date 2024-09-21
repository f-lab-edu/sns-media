from typing import Annotated

from fastapi import BackgroundTasks, Depends, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from src.apis.dependencies import get_session
from src.models.post import Post
from src.models.post_image import PostImage


class PostImageService:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_session)],
        background_tasks: BackgroundTasks,
    ):
        self.session = session
        self.background_tasks = background_tasks

    async def upload_image(self, file: UploadFile, post: Post):
        if not file.filename.endswith(("png", "jpg", "jpeg")):
            raise HTTPException(status_code=400, detail="Invalid file format")

        post_image = PostImage.file_save(file, post.id)
        self.session.add(post_image)
        await self.session.commit()

        return post_image
