from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseRepository
from app.db.models import VideoItem


class VideoItemRepository(BaseRepository[VideoItem, None, None]):
    def __init__(self):
        super().__init__(VideoItem)

    async def get_nearest(self, session: AsyncSession, embedding):
        query = select(self.model.id, self.model.embedding_text.cosine_distance(embedding)).order_by(self.model.embedding_text.cosine_distance(embedding))
        result = await session.execute(query)
        return result.scalar()
