from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class VideoLinkRequest(BaseModel):
    link: str


class VideoItem(BaseModel):
    link: str
    created: datetime
    uuid: UUID
    embedding_text: list[float]


class VideoFrame(BaseModel):
    video_item_id: UUID
    id: UUID
    embedding: list[float]


class VideoLinkResponse(BaseModel):
    is_duplicate: bool
    duplicate_for: str
