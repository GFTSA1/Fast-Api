"""add all columns to posts

Revision ID: 385376e90693
Revises: 262c678a4060
Create Date: 2025-01-15 17:08:05.134377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '385376e90693'
down_revision: Union[str, None] = '262c678a4060'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False))
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
