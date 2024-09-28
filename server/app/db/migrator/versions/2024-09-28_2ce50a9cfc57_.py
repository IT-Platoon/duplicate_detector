"""empty message

Revision ID: 2ce50a9cfc57
Revises: ad3bc9db1da0
Create Date: 2024-09-28 15:34:35.890789

"""
import csv

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy
from sqlalchemy.dialects import postgresql

from app.services.model import ModelVideo2Frames

# revision identifiers, used by Alembic.
revision = '2ce50a9cfc57'
down_revision = 'ad3bc9db1da0'
branch_labels = None
depends_on = None

TABLES = {
    "video_item": sa.table(
        "video_item",
        sa.column('id', postgresql.UUID(as_uuid=True)),
        sa.column('link', sa.TEXT()),
        sa.column('created', postgresql.TIMESTAMP(timezone=True)),
    ),
    "video_frame": sa.table(
        "video_frame",
        sa.column('id', postgresql.UUID(as_uuid=True)),
        sa.column('video_item_id', postgresql.UUID(as_uuid=True)),
        sa.column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=512)),
    ),
}


def upgrade() -> None:
    model = ModelVideo2Frames()
    video_items, video_frames = [], []
    with open(f'./migrator/train.csv', newline='') as csvfile:
        table_reader = csv.reader(csvfile)
        fields = ["created", "uuid", "link", "is_duplicate"]
        iterate = 0
        count = 0
        for row in table_reader:
            if not iterate:
                iterate += 1
                continue
            row_data = {}
            for index, value in enumerate(row):
                if index > 3:
                    break
                row_data[fields[index]] = value
                if row_data.get("is_duplicate", None) is True:
                    continue
            row_data["id"] = row_data["uuid"]
            row_data.pop("uuid")
            row_data.pop("is_duplicate")
            video_items.append(row_data)

            count += 1
            if count == 120:
                break

        for item in video_items:
            dataframe = model.video2frames2embeddings(
                item["link"],
                get_every_sec_frame=2.5,
            )
            for index, row in dataframe.iterrows():
                row_data = {
                    "video_item_id": item["id"],
                    "embedding": row["embedding_data"],
                }
                video_frames.append(row_data)
        op.bulk_insert(TABLES["video_item"], video_items)
        op.bulk_insert(TABLES["video_frame"], video_frames)


def downgrade() -> None:
    connection = op.get_bind()
    for _, table in TABLES.items():
        connection.execute(sa.delete(table))
