from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import BaseTable


class VideoFrame(BaseTable):
    __tablename__ = "video_frame"
    __table_args__ = (
        Index(
            "ix_video_item_embedding_video",
            "embedding",
            postgresql_using='hnsw',
            postgresql_ops={'embedding': 'vector_cosine_ops'}
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=func.gen_random_uuid(),
        doc="Unique index of element (type UUID)",
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
