from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class VideoLinkRequest(BaseModel):
    link: str


class VideoItem(VideoLinkRequest):
    created: datetime
    uuid: UUID


class VideoLinkResponse(BaseModel):
    is_duplicate: bool
    duplicate_for: UUID
