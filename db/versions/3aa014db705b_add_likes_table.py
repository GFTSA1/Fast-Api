"""add likes table

Revision ID: 3aa014db705b
Revises: 385376e90693
Create Date: 2025-01-15 17:37:09.008922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3aa014db705b'
down_revision: Union[str, None] = '385376e90693'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('likes',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    op.alter_column('posts', 'content',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               nullable=False)


def downgrade() -> None:
    op.alter_column('posts', 'content',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               nullable=True)
    op.drop_table('likes')

