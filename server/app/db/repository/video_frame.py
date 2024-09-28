from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from app.db.models import VideoFrame


class VideoFrameRepository(BaseRepository[VideoFrame, None, None]):
    def __init__(self):
        super().__init__(VideoFrame)

    async def get_nearest(self, session: AsyncSession, embedding):
        query = select(self.model.video_item_id, self.model.embedding.cosine_distance(embedding)).order_by(self.model.embedding.cosine_distance(embedding))
        result = await session.execute(query)
        return result.scalar()
