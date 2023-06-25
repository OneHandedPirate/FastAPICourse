"""add columns to post table

Revision ID: 676d33a4ece6
Revises: ad001389d62c
Create Date: 2023-06-25 16:07:51.517359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '676d33a4ece6'
down_revision = 'ad001389d62c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('published',
                                    sa.Boolean(),
                                    nullable=False,
                                    server_default='TRUE'),)
    op.add_column('post', sa.Column('created_at',
                                    sa.TIMESTAMP(timezone=True),
                                    nullable=False,
                                    server_default=sa.text('now()')),)


def downgrade() -> None:
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
