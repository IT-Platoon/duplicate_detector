from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseTable


class VideoFrame(BaseTable):
    __tablename__ = "video_frame"
    __table_args__ = (
        Index(
            "ix_video_item_embedding",
            "embedding",
            postgresql_using='ivfflat',
            postgresql_ops={'embedding': 'vector_l2_ops'}
        ),
    )

    video_item_id = Column(
        "video_item_id",
        UUID(as_uuid=True),
        ForeignKey("video_item.id"),
        nullable=False,
    )
    embedding = Column(
        "embedding",
        Vector(512),
        nullable=True,
    )

    video_item = relationship(
        "VideoItem",
        back_populates="video_frames",
        lazy="joined",
    )
