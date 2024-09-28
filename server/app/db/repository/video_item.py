from .base import BaseRepository
from app.db.models import VideoItem
from app.schemas.detection import VideoItem as VideoItemSchema


class VideoItemRepository(BaseRepository[VideoItem, VideoItemSchema, None]):
    def __init__(self):
        super().__init__(VideoItem)

