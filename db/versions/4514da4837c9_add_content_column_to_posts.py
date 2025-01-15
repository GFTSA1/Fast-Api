"""add content column to posts

Revision ID: 4514da4837c9
Revises: 2d29524812af
Create Date: 2025-01-15 16:43:46.367096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4514da4837c9'
down_revision: Union[str, None] = '2d29524812af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('posts', 'content')
