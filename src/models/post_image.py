import os
import uuid

from fastapi import UploadFile
from sqlmodel import Field, SQLModel

UPLOAD_DIR = "static/images/"


class PostImage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    file_name: str = Field(default=None, nullable=False)
    file_url: str = Field(default=None, nullable=False)
    post_id: int = Field(foreign_key="post.id", nullable=True)

    @classmethod
    def file_save(cls, file: UploadFile, post_id: int) -> "PostImage":
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        content = file.read()
        filename = f"{str(uuid.uuid4())}.jpg"  # uuid로 유니크한 파일명으로 변경
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
            fp.write(content)

        return cls(file_name=filename, file_url=file_path, post_id=post_id)
